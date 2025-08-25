
import datetime
import pandas as pd
import re
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawlerserver.settings')
django.setup()

import datetime
import pandas as pd
import re
import json

def format_timedelta_human_readable(timedelta_obj):
    """
    Converts a timedelta object into a human-readable string (e.g., "1 day 2 hours 30 minutes").
    """
    if timedelta_obj is None:
        return "N/A"

    total_seconds = int(timedelta_obj.total_seconds())
    if total_seconds == 0:
        return "Less than a second"

    days = total_seconds // (24 * 3600)
    total_seconds %= (24 * 3600)
    hours = total_seconds // 3600
    total_seconds %= 3600
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    # Always include seconds if total_seconds > 0, or if it's the only non-zero part
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return " ".join(parts) if parts else "Less than a second"


def analyze_instagram_logs_no_pandas(log_data):
    """
    Analyzes Instagram bot logs to generate a report for each run ID,
    including scraped data counts, specific exception reasons,
    bot login status, and download failure details.

    Args:
        log_data (dict): A dictionary where keys are run_ids and values are lists of log entries.

    Returns:
        dict: A dictionary containing reports for each run_id.
    """
    reports = {}

    for run_id, logs in log_data.items():
        processed_logs = []
        for log in logs:
            log_copy = log.copy()
            if isinstance(log_copy.get('datetime'), (int, float)): # Convert Unix timestamp (milliseconds) to datetime
                log_copy['datetime'] = datetime.datetime.fromtimestamp(log_copy['datetime'] / 1000)
            elif isinstance(log_copy.get('datetime'), pd.Timestamp):
                log_copy['datetime'] = log_copy['datetime'].to_pydatetime()
            elif isinstance(log_copy.get('datetime'), str):
                log_copy['datetime'] = datetime.datetime.fromisoformat(log_copy['datetime'])
            processed_logs.append(log_copy)

        sorted_logs = sorted(processed_logs, key=lambda x: x['datetime'])

        report = {
            "run_id": run_id,
            "total_run_time_of_this_instance": "N/A",
            "total_run_time_seconds": 0,
            "exception": "No exception",
            "specific_exception_reason": "N/A",
            "has_billing_exception": False,
            "bot_username": "N/A",
            "last_log_details": "N/A",
            "task_completion_status": "Incomplete (Stopped Without Completion Log)",
            "bot_login_status_for_run": False,
            "scraped_data_summary": {},
            "data_enrichment_summary":{},
            "start_datetime": None,
            "end_datetime": None,
            "found_next_page_info_count": 0,
            "next_page_info_not_found_count": 0,
            "saved_file_count": 0,
            "downloaded_file_count": 0,
            "storage_house_upload_failures":0,
            "storage_house_uploads":0,
            "failed_to_download_file_count": 0, # New counter
            "failed_downloads_details": [], # New list for failed download details
            "error_details": []
        }

        if sorted_logs:
            start_time = sorted_logs[0]['datetime']
            end_time = sorted_logs[-1]['datetime']
            total_task_time_delta = end_time - start_time
            report["total_run_time_of_this_instance"] = str(total_task_time_delta)
            report["total_run_time_seconds"] = total_task_time_delta.total_seconds()
            report["start_datetime"] = start_time
            report["end_datetime"] = end_time

            last_log = sorted_logs[-1]
            if last_log.get('type') == 'error' and last_log.get('string'):
                report["last_log_details"] = f"Type: {last_log.get('type')}, Message: {last_log['string'].get('args', [''])[0]}"
            elif last_log.get('type') == 'exception' and last_log.get('string'):
                report["last_log_details"] = f"Type: {last_log.get('type')}, Name: {last_log['string'].get('name', 'Unknown')}, Message: {last_log['string'].get('args', [''])[0]}"
            else:
                report["last_log_details"] = f"Type: {last_log.get('type')}"

            """             if last_log.get('type') == 'failed_login':
                report["bot_login_status_for_run"] = "Logged Out"
            else:
                report["bot_login_status_for_run"] = "Logged In" """


        found_bot_username = None
        for log in sorted_logs:
            if 'bot_username' in log and not pd.isna(log['bot_username']):
                found_bot_username = log['bot_username']
                break
        if found_bot_username:
            report["bot_username"] = found_bot_username
        elif any(log.get('service') == 'instagram' for log in sorted_logs):
            report["bot_username"] = "Instagram Bot (username not specified in logs)"

        exception_found = False
        for log in sorted_logs:
            if log.get('type') == 'exception' or log.get('type') == 'exception_encountered':
                exception_info = log.get('string', {})
                
                from analysis_helpers import create_exception_report_entry
                report['exception']=create_exception_report_entry(log)
               
                report["task_completion_status"] = "Failed (Exception Encountered)"
                exception_found = True

                if "insufficient funds" in str(exception_info).lower():
                    report["specific_exception_reason"] = "Insufficient Funds"
                    report["has_billing_exception"] = True
                elif "quota exceeded" in str(exception_info).lower():
                    report["specific_exception_reason"] = "API Quota Exceeded"
                    report["has_billing_exception"] = True
                break

        if not exception_found:
            for log in sorted_logs:
                if log.get('type') == 'task_run_completed':
                    report["task_completion_status"] = "Completed Successfully"
                    break

        for log in sorted_logs:
            if log.get('type') == 'data_acquired':
                for metric in ['total_users_scraped', 'total_posts_scraped', 'pages_scraped', 'comments_scraped']:
                    if metric in log and isinstance(log[metric], (int, float)):
                        report["scraped_data_summary"][metric] = report["scraped_data_summary"].get(metric, 0) + log[metric]
                        
                        

                for metric in ['total_rows','total_rows_with_missing_column','total_gpt_responses', 'total_empty_responses', 'total_partial_responses', 'exception_in_openai_api','total_complete_responses']:
                    if metric in log and isinstance(log[metric], (int, float)):
                        report["data_enrichment_summary"][metric] = report["scraped_data_summary"].get(metric, 0) + log[metric]

            elif log.get('type') == 'found_next_page_info':
                report["found_next_page_info_count"] += 1
            elif log.get('type') == 'next_page_info_not_found':
                report["next_page_info_not_found_count"] += 1
            elif log.get('type') == 'saved_file_to_local_storage':
                report["saved_file_count"] += 1
            elif log.get('type') == 'failed_to_save_file_to_storage_house':
                report["storage_house_upload_failures"] += 1
            elif log.get('type') == 'saved_file_to_storage_house':
                report["storage_house_uploads"] += 1
            elif log.get('type') == 'downloaded_file':
                report["downloaded_file_count"] += 1
            elif log.get('type') == 'failed_to_download_file': # Handle new log type
                report["failed_to_download_file_count"] += 1
                report["failed_downloads_details"].append({
                    "url": log.get('url', 'N/A'),
                    "error": log.get('error', 'No specific error message'),
                    "datetime": str(log['datetime'])
                })
            elif log.get('type') == 'error':
                error_traceback = log.get('traceback', '')
                match = re.search(r'File ".*[\\/]([^\\/]+)\.py", line \d+, in (\w+)', error_traceback)
                error_module_function = "Unknown"
                if match:
                    error_module = match.group(1)
                    error_function = match.group(2)
                    error_module_function = f"Module: {error_module}, Function: {error_function}"
                report["error_details"].append({
                    "message": log.get('string', {}) if log.get('string') else "No specific message",
                    "module_function": error_module_function,
                    "datetime": str(log['datetime'])
                })

        return report

    return reports



def analyze_overall_task_status(individual_run_reports):
    """
    Analyzes the overall task status and total runtime based on individual run reports,
    including scraped data totals, specific exception reasons,
    overall bot login status, datetime range, and download failure summary.

    Args:
        individual_run_reports (dict): A dictionary of reports generated by analyze_instagram_logs_no_pandas.

    Returns:
        dict: A dictionary containing the overall task status and total runtime.
    """
    overall_status = "Successful"
    earliest_start_time = None
    latest_end_time = None 
    completed_runs_count = 0
    failed_runs_count = 0
    incomplete_runs_count = 0
    exceptions_encountered = []
    specific_exception_reasons_overall = []
    
    overall_scraped_data_total = {} 
    overall_data_enrichment_total={}
    overall_found_next_page_info_count = 0
    overall_next_page_info_not_found_count = 0
    overall_saved_file_count = 0
    overall_downloaded_file_count = 0
    overall_failed_to_download_file_count = 0 # New overall counter
    overall_failed_downloads_summary = [] # New overall summary for failed downloads
    overall_errors_summary = []
    overall_total_run_time_seconds_sum = 0
    
    last_status_of_task_run = "Unspecified - No runs completed"
    overall_bot_login_status = "Unknown (No Runs)"
    overall_has_billing_exception = False
    
    overall_latest_log_datetime = datetime.datetime.min
    overall_latest_log_details = "N/A"
    overall_latest_bot_login_status = "Unknown"


    any_run_failed = False
    any_run_incomplete = False
    all_runs_completed_successfully = True

    for run_id, report in individual_run_reports.items():
        if report["task_completion_status"] == "Completed Successfully":
            completed_runs_count += 1
        elif report["task_completion_status"] == "Failed (Exception Encountered)":
            failed_runs_count += 1
            any_run_failed = True
            exceptions_encountered.append(report["exception"])
            all_runs_completed_successfully = False
            if report["specific_exception_reason"] != "N/A":
                specific_exception_reasons_overall.append(report["specific_exception_reason"])
            if report["has_billing_exception"]:
                overall_has_billing_exception = True
        elif report["task_completion_status"] == "Incomplete (Stopped Without Completion Log)":
            incomplete_runs_count += 1
            any_run_incomplete = True
            all_runs_completed_successfully = False
            if report["has_billing_exception"]:
                overall_has_billing_exception = True


        if isinstance(report["scraped_data_summary"], dict):
            for key, value in report["scraped_data_summary"].items():
                overall_scraped_data_total[key] = overall_scraped_data_total.get(key, 0) + value
        if isinstance(report["data_enrichment_summary"], dict):
            for key, value in report["data_enrichment_summary"].items():
                overall_data_enrichment_total[key] = overall_data_enrichment_total.get(key, 0) + value

        overall_found_next_page_info_count += report["found_next_page_info_count"]
        overall_next_page_info_not_found_count += report["next_page_info_not_found_count"]
        overall_saved_file_count += report["saved_file_count"]
        overall_downloaded_file_count += report["downloaded_file_count"]
        overall_failed_to_download_file_count += report["failed_to_download_file_count"] # Aggregate new counter
        overall_failed_downloads_summary.extend(report["failed_downloads_details"]) # Aggregate new details
        overall_errors_summary.extend(report["error_details"])
        overall_total_run_time_seconds_sum += report["total_run_time_seconds"]
        from analysis_helpers import make_datetimes_timezone_aware
        if report["start_datetime"]:
            if earliest_start_time is None or make_datetimes_timezone_aware(report["start_datetime"]) < make_datetimes_timezone_aware(earliest_start_time):
                earliest_start_time = report["start_datetime"]
        
        if report["end_datetime"]:
            if latest_end_time is None or make_datetimes_timezone_aware(report["end_datetime"]) >  make_datetimes_timezone_aware(latest_end_time):
                latest_end_time = report["end_datetime"]
            
            if make_datetimes_timezone_aware(report["end_datetime"]) > make_datetimes_timezone_aware( overall_latest_log_datetime):
                overall_latest_log_datetime = report["end_datetime"]
                overall_latest_log_details = report["last_log_details"]
                overall_latest_bot_login_status = report["bot_login_status_for_run"]


    total_task_runtime_timedelta = datetime.timedelta(seconds=overall_total_run_time_seconds_sum)
    total_task_runtime_text = str(total_task_runtime_timedelta)
    total_task_runtime_human_readable = format_timedelta_human_readable(total_task_runtime_timedelta)
    
    overall_bot_login_status = overall_latest_bot_login_status

    if any_run_failed:
        overall_status = "Failed"
    elif any_run_incomplete and completed_runs_count == 0:
        overall_status = "Incomplete"
    elif completed_runs_count > 0 and (any_run_failed or any_run_incomplete):
        overall_status = "Partially Completed / Problematic"
    elif all_runs_completed_successfully and len(individual_run_reports) > 0:
        overall_status = "Completed Successfully"
    elif len(individual_run_reports) == 0:
        overall_status = "No Runs Initiated"
        overall_latest_log_details = "No logs available for task."
        total_task_runtime_text = "N/A"
        overall_total_run_time_seconds_sum = 0
        total_task_runtime_human_readable = "N/A"

    if not overall_scraped_data_total: 
        overall_scraped_data_total_summary = "No scraped data reported"
    else:
        overall_scraped_data_total_summary = overall_scraped_data_total
    if not overall_data_enrichment_total: 
        overall_data_enrichment_summary = "No Data Enrichment Reported"
    else:
        overall_data_enrichment_summary=overall_data_enrichment_total

    billing_issue_resolved_status = "N/A (No billing issues encountered)"
    if overall_has_billing_exception:
        sorted_runs_by_end_time = sorted(individual_run_reports.values(), key=lambda x: x['end_datetime'] if x['end_datetime'] else datetime.datetime.min)
        
        if sorted_runs_by_end_time and (sorted_runs_by_end_time[-1]["task_completion_status"] == "Completed Successfully" and not sorted_runs_by_end_time[-1]["has_billing_exception"]):
            billing_issue_resolved_status = "Possibly Resolved (Last chronological run was successful and free of billing issues)"
        else:
            billing_issue_resolved_status = "Unresolved (Billing issue encountered and last chronological run was not successful or still had billing issues)"
    

    overall_report = {
        "overall_task_status": overall_status,
        "report_start_datetime": earliest_start_time.isoformat() if earliest_start_time else "N/A",
        "report_end_datetime": latest_end_time.isoformat() if latest_end_time else "N/A",
        "total_task_runtime": total_task_runtime_text,
        "total_task_runtime_seconds": overall_total_run_time_seconds_sum, 
        "total_task_runtime_human_readable": total_task_runtime_human_readable,
        "number_of_runs_initiated": len(individual_run_reports),
        "completed_runs_count": completed_runs_count,
        "failed_runs_count": failed_runs_count,
        "incomplete_runs_count": incomplete_runs_count,
        "overall_scraped_data_total": overall_scraped_data_total_summary,
        "data_enrichment_summary":overall_data_enrichment_summary,
        "overall_found_next_page_info_count": overall_found_next_page_info_count,
        "overall_next_page_info_not_found_count": overall_next_page_info_not_found_count,
        "overall_saved_file_count": overall_saved_file_count,
        "overall_downloaded_file_count": overall_downloaded_file_count,
        "overall_failed_to_download_file_count": overall_failed_to_download_file_count, # New field
        "overall_failed_downloads_summary": overall_failed_downloads_summary if overall_failed_downloads_summary else "No failed downloads reported", # New field
        "overall_bot_login_status": overall_bot_login_status,
        "overall_errors_summary": overall_errors_summary if overall_errors_summary else "No non-fatal errors across all runs",
        "exceptions_summary": exceptions_encountered if exceptions_encountered else "No exceptions across all runs",
        "specific_exception_reasons_overall": specific_exception_reasons_overall if specific_exception_reasons_overall else "N/A",
        "billing_issue_resolved_status": billing_issue_resolved_status,
        "last_status_of_task_run": overall_latest_log_details
    }

    return overall_report

def format_report_for_json_output(overall_report):
    """
    Flattens the overall task report into a single-level dictionary suitable for JSON output,
    avoiding nested lists/dicts for direct Google Sheet compatibility.
    """
    flattened_report = {
        "Overall Task Status": overall_report["overall_task_status"],
        "Report Start Datetime": overall_report["report_start_datetime"],
        "Report End Datetime": overall_report["report_end_datetime"],
        "Total Task Runtime (Text)": overall_report["total_task_runtime"],
        "Total Task Runtime (Seconds)": overall_report["total_task_runtime_seconds"],
        "Total Task Runtime (Human Readable)": overall_report["total_task_runtime_human_readable"],
        "Runs Initiated": overall_report["number_of_runs_initiated"],
        "Runs Completed": overall_report["completed_runs_count"],
        "Runs Failed (Exception)": overall_report["failed_runs_count"],
        "Runs Incomplete": overall_report["incomplete_runs_count"],
        "Found Next Page Info Count": overall_report["overall_found_next_page_info_count"],
        "Next Page Info Not Found Count": overall_report["overall_next_page_info_not_found_count"],
        "Saved File Count": overall_report["overall_saved_file_count"],
        "Downloaded File Count": overall_report["overall_downloaded_file_count"],
        "Failed Download Count": overall_report["overall_failed_to_download_file_count"], # New field
        "Overall Bot Login Status": overall_report["overall_bot_login_status"],
        "Last Status of Task": overall_report["last_status_of_task_run"],
        "Billing Issue Resolution Status": overall_report["billing_issue_resolved_status"],
        "Data Enrichment Summary":overall_report["data_enrichment_summary"]
    }

    # Flatten scraped data with corrected naming and no default columns
    if isinstance(overall_report["overall_scraped_data_total"], dict):
        for key, value in overall_report["overall_scraped_data_total"].items():
            if key.startswith('total_'):
                display_key = f"Total {key.replace('total_', '', 1).replace('_', ' ').title()}"
            else:
                display_key = key.replace('_', ' ').title()
            flattened_report[display_key] = value
    else:
        flattened_report["Scraped Data Summary"] = overall_report["overall_scraped_data_total"]
    flattened_report["Scraped Data Summary"] = overall_report["overall_scraped_data_total"]

    # Flatten non-fatal errors
    if isinstance(overall_report["overall_errors_summary"], list) and overall_report["overall_errors_summary"]:
        error_messages = []
        for error in overall_report["overall_errors_summary"]:
            msg = error.get('message', 'N/A')
            mod_func = error.get('module_function', 'N/A')
            error_messages.append(f"'{msg}' (Module/Func: {mod_func})")
        flattened_report["Non-Fatal Errors Summary"] = f"{len(error_messages)} error(s) detected: " + "; ".join(error_messages)
    else:
        flattened_report["Non-Fatal Errors Summary"] = overall_report["overall_errors_summary"]

    # Flatten exceptions summary
    if isinstance(overall_report["exceptions_summary"], list) and overall_report["exceptions_summary"]:
        exception_messages = []
        for exc in overall_report["exceptions_summary"]:
            name = exc.get('name', 'Unknown')
            message = exc.get('message', 'No specific message')
            exception_messages.append(f"{name} - '{message}'")
        flattened_report["Exceptions Summary"] = f"{len(exception_messages)} exception(s) detected: " + "; ".join(exception_messages)
    else:
        flattened_report["Exceptions Summary"] = overall_report["exceptions_summary"]

    # Flatten specific exception reasons
    if isinstance(overall_report["specific_exception_reasons_overall"], list) and overall_report["specific_exception_reasons_overall"]:
        flattened_report["Specific Exception Reasons"] = ", ".join(sorted(list(set(overall_report["specific_exception_reasons_overall"]))))
    else:
        flattened_report["Specific Exception Reasons"] = overall_report["specific_exception_reasons_overall"]
    
    # Flatten failed downloads summary
    if isinstance(overall_report["overall_failed_downloads_summary"], list) and overall_report["overall_failed_downloads_summary"]:
        failed_download_messages = []
        for dl_fail in overall_report["overall_failed_downloads_summary"]:
            url = dl_fail.get('url', 'N/A')
            error_msg = dl_fail.get('error', 'No specific error')
            failed_download_messages.append(f"URL: '{url}', Error: '{error_msg}'")
        flattened_report["Failed Downloads Summary"] = f"{len(failed_download_messages)} failed download(s): " + "; ".join(failed_download_messages)
    else:
        flattened_report["Failed Downloads Summary"] = overall_report["overall_failed_downloads_summary"]

    return flattened_report


# --- Test Data (Added failed_to_download_file log) ---



# Step 1: Analyze each individual run
def analyze_task(task_dict,report_creation_task_uuid):
        log_data={}
        task=task_dict
        # --- Test Data with all new log types ---
        from base.storage_sense import Saver
        import pandas as pd
        s=Saver()
        consumed_inputs=s.get_consumed_blocks(id=task.get('uuid'))
        resp=s.read_task_outputs_redundant(uuid=task.get('uuid'),block_name='logs',exclude_blocks=consumed_inputs,keys=True)
        logs_dict={}
        consumed_inputs=[]
        for key, value in resp.items():
            
            row=value[0]
            if not log_data.get(row.get('run_id'),False):
                log_data.update({row['run_id']:[]})
            log_data[row['run_id']].append(row)
            consumed_inputs.append(key)
       

        # Step 1: Analyze each individual run

        individual_run_reports = analyze_instagram_logs_no_pandas(log_data)
        s.file_extension='.json'
        s.create_task_outputs('12',data=individual_run_reports)
        print(individual_run_reports)
        """  overall_task_report = analyze_overall_task_status(individual_run_reports)
        print(overall_task_report) """
        for id in consumed_inputs:
            s.add_output_block_to_consumed(id=task.get('uuid'),output_block=id)
        #flattend_report=format_report_for_json_output(overall_task_report)
        
        #return flattend_report
import uuid
#print(analyze_task(task_dict={'uuid':'6f2ec27e-7216-11f0-9256-e840f2360fa3'},report_creation_task_uuid=uuid.uuid1()))
def summarize_run_log_folder(task_dict, report_creation_task_uuid):
    from base.storage_sense import Saver
    from collections import defaultdict, deque

    def get_latency_seconds(end, start):
        try:
            return round((end - start).total_seconds(), 2)
        except AttributeError:
            return round(end - start, 2)

    log_data = {}
    task = task_dict
    s = Saver()

    consumed_inputs = s.get_consumed_blocks(id=task.get('uuid'))
    resp = s.read_task_outputs_for_run_id(
        uuid=task.get('uuid'),
        run_id=task.get('run_id'),
        exclude_blocks=consumed_inputs,
        keys=True
    )

    consumed_inputs = []
    for key, value in resp.items():
        row = value[0]
        run_id = row.get('run_id')

        if run_id not in log_data:
            log_data[run_id] = []

        log_data[run_id].append(row)
        consumed_inputs.append(key)

    for id in consumed_inputs:
        s.add_output_block_to_consumed(id=task.get('uuid'),output_block=id)
        
    logs = []
    for log_list in log_data.values():
        logs.extend(log_list)
       

    logs = sorted((log for log in logs if isinstance(log, dict) and "timestamp" in log), key=lambda x: x["timestamp"])


    if not logs:
        print("No valid logs found.")
        

    MIN_GAP = 2  # seconds — minimum time between similar events to be considered distinct

    summary = {
        
        "run_id": task.get('run_id'),
        "task_id": task.get('uuid') ,
        "service": task.get('service'),
        "end_point": task.get('end_point'),
        "data_point": task.get('data_point'),
        "page_load_summary": {},
        "scraping_summary":{},
        "download_summary":{},
        "request_cache_summary":{},
        "proxy_summary":{},
        "authorization_summary":{},
        "billing_issue_summary":{},
        "api_requests_summary":{},
        "critical_events": [],
        "total_logs": len(logs),
        "page_detection_details": defaultdict(dict),  # Initialize here
        "locate_element_xpaths": defaultdict(dict),  # Initialize here
        "attempt_failed_errors": []
    }
    if logs:
        summary.update({"report_start_datetime" : logs[0]['timestamp'],
        "report_end_datetime": logs[-1]['timestamp']})

    for log in logs:
        if log.get("critical", False):
            summary["critical_events"].append(log)

    for log in logs:
        if log.get("login_attempt_failed", False) or log.get('2fa_attempt_failed',False):
     
            summary["attempt_failed_errors"].append(log)

    # -------------------- Page Load Section --------------------
    page_load_tracker = defaultdict(deque)
    page_refresh_tracker = defaultdict(deque)

    last_start_time = {}
    last_success_time = {}

    for log in logs:
        log_type = log.get("type")
        page = log.get("page")
        timestamp = log.get("timestamp")
        if log.get("end_point") != "page_load":
            continue
 

        page_summary = summary["page_load_summary"].setdefault(page, {
            "start_attempts": 0,
            "success_page_load": 0,
            "total_page_load_time": 0.0,
            "refresh_success": 0,
            "refresh_failed": 0,
            "load_failed": 0,
            "failed_attempts": 0,
            "exceptions": []
        })

        if log_type == "page_loading_start":
            last_ts = last_start_time.get(page)
            if not last_ts or get_latency_seconds(timestamp, last_ts) > MIN_GAP:
                page_summary["start_attempts"] += 1
                page_load_tracker[page].append(timestamp)
                last_start_time[page] = timestamp

        elif log_type == "page_loaded_successfully":
            last_ts = last_success_time.get(page)
            if not last_ts or get_latency_seconds(timestamp, last_ts) > MIN_GAP:
                if page_load_tracker[page]:
                    start_ts = page_load_tracker[page].popleft()
                    latency = get_latency_seconds(timestamp, start_ts)
                    page_summary["total_page_load_time"] += latency
                    page_summary["success_page_load"] += 1
                    last_success_time[page] = timestamp

        elif log_type == "page_refresh_start":
            page_refresh_tracker[page].append(timestamp)

        elif log_type == "page_refresh_successfully":
            page_summary["refresh_success"] += 1
            if page_refresh_tracker[page]:
                start_ts = page_refresh_tracker[page].popleft()
                latency = get_latency_seconds(timestamp, start_ts)
                page_summary["total_page_load_time"] += latency

        elif log_type == "refresh_failed":
            page_summary["refresh_failed"] += 1

        elif log_type == "page_not_load":
            page_summary["load_failed"] += 1

        elif log_type == "exception":
            page_summary["exceptions"].append(log)
        
        
        elif log_type == "page_failed_to_load_after_retries":
            attempts = log.get("max_attempts", 1)
            page_summary["load_failed"] += 1
            page_summary["failed_attempts"] += attempts

    # Round total load time
    for page_data in summary["page_load_summary"].values():
        if "total_page_load_time" in page_data:
            page_data["total_page_load_time"] = round(page_data["total_page_load_time"], 2)

    # Clean empty entries
    summary["page_load_summary"] = {
        page: data for page, data in summary["page_load_summary"].items() if data
    }
    # -------------------- Login Section --------------------

    login_summary = {
        "total_login_attempts": 0,
        "successful_logins": 0,
        "total_login_time": 0.0,
        "total_failed_logins": 0,
        "total_failed_attempts":0,
        "2fa_attempts": 0,
        "2fa_successes": 0,
        "2fa_failures": 0,
        "2fa_total_time": 0.0,
        "login_exceptions": [],
        "bot_login_status_for_run":""
    }

    first_login_attempt_start = None
    last_login_attempt_finish = None
    two_fa_start_tracker = deque()

    attempt_start = None
    last_attempt_finish = None
    login_attempt_latencies = []
    login_attempt_gaps = []
    total_gap_time = 0.0
  

    for log in logs:
        if log.get("end_point") != "login":
            continue
        

        lt = log.get("type")
        ts = log.get("timestamp")

        if lt == "login_attempt_started":
            login_summary["total_login_attempts"] += 1

            # Track the first login start time
            if first_login_attempt_start is None or ts < first_login_attempt_start:
                first_login_attempt_start = ts

            # If a previous attempt finished, calculate the gap
            if last_attempt_finish:
                gap = get_latency_seconds(ts, last_attempt_finish)
                login_attempt_gaps.append(gap)
                total_gap_time += gap

            attempt_start = ts

        elif lt == "login_attempt_finished":
            # Update last login finish
            if last_login_attempt_finish is None or ts > last_login_attempt_finish:
                last_login_attempt_finish = ts

            # Track current finish as "last_attempt_finish" for next gap
            last_attempt_finish = ts

            if attempt_start:
                latency = get_latency_seconds(ts, attempt_start)
                login_attempt_latencies.append(latency)
                attempt_start = None  # Reset

        elif lt == "login_success":
            login_summary["successful_logins"] += 1

        elif lt == "internet_issue":
            login_summary["total_failed_logins"] += 1

        elif lt == "incorrect_password":
            login_summary["total_failed_logins"] += 1

        elif lt == "username_or_password_not_found":
            login_summary["total_failed_logins"] += 1

        elif lt == "profile_not_found":
            login_summary["total_failed_logins"] += 1

        elif lt == "2fa_start":
            login_summary["2fa_attempts"] += 1
            two_fa_start_tracker.append(ts)

        elif lt == "2fa_success":
            login_summary["2fa_successes"] += 1
            if two_fa_start_tracker:
                start_ts = two_fa_start_tracker.popleft()
                login_summary["2fa_total_time"] += get_latency_seconds(ts, start_ts)

        elif lt == "2fa_failed":
            login_summary["2fa_failures"] += 1
            if two_fa_start_tracker:
                two_fa_start_tracker.pop()

        elif lt == "2fa_failed_after_retry":
            login_summary["total_failed_logins"] += 1

        elif lt == "internet_issue":
            login_summary["total_failed_logins"] += 1

        elif lt == "failed_to_identify_active_page":
            login_summary["total_failed_logins"] += 1

        elif lt == "failed_to_identify_active_page_2fa_retry":
            login_summary["total_failed_logins"] += 1


        elif lt == "exception":
            login_summary["login_exceptions"].append(log)

    # Final summary calculations
    if first_login_attempt_start and last_login_attempt_finish:
        login_summary["total_login_time"] = round(
            get_latency_seconds(last_login_attempt_finish, first_login_attempt_start), 2
        )
    else:
        login_summary["total_login_time"] = 0.0


    # ✅ Set bot login status
    if login_summary["successful_logins"] > 0:
        login_summary["bot_login_status_for_run"] = "Logged In"
    else:
        login_summary["bot_login_status_for_run"] = "Failed"

    summary["login_summary"] = login_summary

    # -------------------- Page Detection Summary (Nested by Page) --------------------
    page_detection_exceptions = []

    for log in logs:
        if log.get("end_point") != "page_detect":
            continue

        log_type = log.get("type")
        timestamp = log.get("timestamp")
        xpath = log.get("xpath", [])
        page = log.get("page")  # Page URL from the log

        if not page or not isinstance(xpath, list):
            continue

        # Normalize list of xpaths (flatten if nested)
        flat_xpaths = [
            x for item in xpath
            for x in (item if isinstance(item, list) else [item])
            if isinstance(x, str)
        ]

        if page not in summary["page_detection_details"]:
            summary["page_detection_details"][page] = {
                "xpaths": defaultdict(lambda: {
                    "detection_attempts": 0,
                    "identified": 0,
                    "not_identified": 0,
                    "total_detection_time": 0.0
                }),
                "detection_start_tracker": defaultdict(list),
                "exceptions": []
            }

        page_detection_data = summary["page_detection_details"][page]
        xpath_data = page_detection_data["xpaths"]
        detection_start_tracker = page_detection_data["detection_start_tracker"]

        for x in flat_xpaths:
            if log_type == "page_detection_started":
                xpath_data[x]["detection_attempts"] += 1
                detection_start_tracker[x].append(timestamp)

            elif log_type == "page_identified":
                xpath_data[x]["identified"] += 1
                if detection_start_tracker[x]:
                    start_ts = detection_start_tracker[x].pop(0)
                    latency = get_latency_seconds(timestamp, start_ts)
                    xpath_data[x]["total_detection_time"] += latency

            elif log_type == "page_not_identified":
                xpath_data[x]["not_identified"] += 1
                if detection_start_tracker[x]:
                    start_ts = detection_start_tracker[x].pop(0)
                    latency = get_latency_seconds(timestamp, start_ts)
                    xpath_data[x]["total_detection_time"] += latency
                

            elif log_type == "page_detection_exception":
                page_detection_exceptions.append(log)
                page_detection_data["exceptions"].append(log)
                

    # Round total detection time and cleanup trackers
    for page_data in summary["page_detection_details"].values():
        for xpath, data in page_data["xpaths"].items():
            data["total_detection_time"] = round(data["total_detection_time"], 2)
        if "detection_start_tracker" in page_data:
            del page_data["detection_start_tracker"]


    # -------------------- Locate Element Summary (Nested by Page) --------------------
    locate_element_exceptions = []

    for log in logs:
        if log.get("end_point") != "locate_element":
            continue

        log_type = log.get("type")
        timestamp = log.get("timestamp")
        xpath = log.get("x_path")
        page = log.get("page") # Get page from log

        if not page or not isinstance(xpath, str):
            continue

        if page not in summary["locate_element_xpaths"]:
            summary["locate_element_xpaths"][page] = {
                "xpaths": defaultdict(lambda: {
                    "detection_attempts": 0,
                    "xpath_found": 0,
                    "clicked_xpath": 0,
                    "attr_fetched": 0,
                    "not_found": 0,
                    "exceptions": 0,
                    "click_failed": 0,
                    "total_detection_time": 0.0,
                }),
                "detection_start_tracker": defaultdict(list),
                "exceptions": []
            }
        
        page_locate_data = summary["locate_element_xpaths"][page]
        xpath_data = page_locate_data["xpaths"]
        detection_start_tracker = page_locate_data["detection_start_tracker"]

        if log_type == "xpath_locate_attempt_start":
            xpath_data[xpath]["detection_attempts"] += 1
            detection_start_tracker[xpath].append(timestamp)

        elif log_type in {"xpath_found", "clicked_xpath", "xpath_attr_fetched"}:
            if detection_start_tracker[xpath]:
                start_ts = detection_start_tracker[xpath].pop(0)
                latency = get_latency_seconds(timestamp, start_ts)
                xpath_data[xpath]["total_detection_time"] += latency

            if log_type == "xpath_found":
                xpath_data[xpath]["xpath_found"] += 1
            elif log_type == "clicked_xpath":
                xpath_data[xpath]["clicked_xpath"] += 1
            elif log_type == "xpath_attr_fetched":
                xpath_data[xpath]["attr_fetched"] += 1

        elif log_type == "xpath_not_found":
            xpath_data[xpath]["not_found"] += 1
            if detection_start_tracker[xpath]:
                start_ts = detection_start_tracker[xpath].pop(0)
                latency = get_latency_seconds(timestamp, start_ts)
                xpath_data[xpath]["total_detection_time"] += latency

        elif log_type == "xpath_exception":
            xpath_data[xpath]["exceptions"] += 1
            locate_element_exceptions.append(log)
            page_locate_data["exceptions"].append(log) # Add to page-specific exceptions

        elif log_type == "click_failed":
            xpath_data[xpath]["click_failed"] += 1
            locate_element_exceptions.append(log)
            page_locate_data["exceptions"].append(log) # Add to page-specific exceptions

    # Round total detection time for locate_element_xpaths
    for page_data in summary["locate_element_xpaths"].values():
        for xpath, data in page_data["xpaths"].items():
            data["total_detection_time"] = round(data["total_detection_time"], 2)
        # Remove temporary tracker
        if "detection_start_tracker" in page_data:
            del page_data["detection_start_tracker"]

    # Final structure for page_detection_details and locate_element_xpaths
    # They are already nested by page in the summary, so no further action needed here.
    
    # Store global exceptions
    summary["page_detection_exceptions"] = page_detection_exceptions
    summary["locate_element_exceptions"] = locate_element_exceptions
    
    rep=analyze_instagram_logs_no_pandas(log_data=log_data)
    summary.update(rep)
    return summary


# def format_run_summary_for_json_output(summary):
#     """
#     Flatten the run summary dictionary into a single-level dictionary for JSON output or Google Sheets.
#     """
#     flattened = {}

#     # Basic summary info
#     flattened["Total Logs"] = summary.get("total_logs", 0)
#     flattened["Run Started At"] = summary.get("started_at")

#     # Critical events count and summary
#     critical_events = summary.get("critical_events", [])
#     flattened["Critical Events Count"] = len(critical_events)
#     if critical_events:
#         flattened["Critical Events Summary"] = "; ".join(
#             [f"{ev.get('type', 'Unknown')} @ {ev.get('timestamp')}" for ev in critical_events]
#         )
#     else:
#         flattened["Critical Events Summary"] = "None"

#     # Page load summary flattening
#     page_load_summary = summary.get("page_load_summary", {})
#     for page, stats in page_load_summary.items():
#         prefix = f"Page Load - {page}"
#         flattened[f"{prefix} - Start Attempts"] = stats.get("start_attempts", 0)
#         flattened[f"{prefix} - Successful Loads"] = stats.get("success_page_load", 0)
#         flattened[f"{prefix} - Total Page Load Time"] = round(stats.get("total_page_load_time", 0.0), 2)
#         flattened[f"{prefix} - Refresh Success"] = stats.get("refresh_success", 0)
#         flattened[f"{prefix} - Refresh Failed"] = stats.get("refresh_failed", 0)
#         flattened[f"{prefix} - Load Failed"] = stats.get("load_failed", 0)
#         flattened[f"{prefix} - Failed Attempts"] = stats.get("failed_attempts", 0)
#         flattened[f"{prefix} - Failed Latency"] = round(stats.get("failed_latency", 0.0), 2)
#         # Count exceptions for this page if any
#         exceptions = stats.get("exceptions", [])
#         flattened[f"{prefix} - Exceptions Count"] = len(exceptions)
#         if exceptions:
#             flattened[f"{prefix} - Exceptions Summary"] = "; ".join(
#                 [str(ex.get("message", ex)) for ex in exceptions]
#             )
#         else:
#             flattened[f"{prefix} - Exceptions Summary"] = "None"

#     # Login summary flattening
#     login_summary = summary.get("login_summary", {})
#     if login_summary:
#         flattened["Login - Total Attempts"] = login_summary.get("total_login_attempts", 0)
#         flattened["Login - Successful Logins"] = login_summary.get("successful_logins", 0)
#         flattened["Login - Total Login Time"] = round(login_summary.get("total_login_time", 0.0), 2)
#         flattened["Login - Failed Logins"] = login_summary.get("total_failed_logins", 0)
#         flattened["Login - 2FA Attempts"] = login_summary.get("2fa_attempts", 0)
#         flattened["Login - 2FA Successes"] = login_summary.get("2fa_successes", 0)
#         flattened["Login - 2FA Failures"] = login_summary.get("2fa_failures", 0)
#         flattened["Login - 2FA Total Time"] = round(login_summary.get("2fa_total_time", 0.0), 2)

#         login_exceptions = login_summary.get("login_exceptions", [])
#         flattened["Login - Exceptions Count"] = len(login_exceptions)
#         if login_exceptions:
#             flattened["Login - Exceptions Summary"] = "; ".join(
#                 [f"{ex.get('type', 'Exception')} @ {ex.get('timestamp')}" for ex in login_exceptions]
#             )
#         else:
#             flattened["Login - Exceptions Summary"] = "None"

#     # Page identification summary flattening
#     page_ident_summary = summary.get("page_identification_summary", {})
#     xpaths = page_ident_summary.get("xpaths", {})
#     for xpath, stats in xpaths.items():
#         prefix = f"XPath Detection - {xpath}"
#         flattened[f"{prefix} - Detection Attempts"] = stats.get("detection_attempts", 0)
#         flattened[f"{prefix} - Identified"] = stats.get("identified", 0)
#         flattened[f"{prefix} - Not Identified"] = stats.get("not_identified", 0)
#         flattened[f"{prefix} - Total Detection Time"] = round(stats.get("total_detection_time", 0.0), 2)

#     # Shared exceptions for page detection
#     shared_exceptions = page_ident_summary.get("exceptions", [])
#     flattened["Page Detection - Exceptions Count"] = len(shared_exceptions)
#     if shared_exceptions:
#         flattened["Page Detection - Exceptions Summary"] = "; ".join(
#             [f"{ex.get('type', 'Exception')} @ {ex.get('timestamp')}" for ex in shared_exceptions]
#         )
#     else:
#         flattened["Page Detection - Exceptions Summary"] = "None"

#     return flattened




""" og_data={}
task={'uuid':'637917b2-0ca2-11f0-8545-047c1611323a','data_point':'location_posts','end_point':'location'}
# --- Test Data with all new log types ---
from base.storage_sense import Saver
import pandas as pd
s=Saver()
consumed_inputs=s.get_consumed_blocks(id=task.get('uuid'))
resp=s.read_task_outputs(uuid=task.get('uuid'),block_name='logs',exclude_blocks=consumed_inputs,keys=False)
logs_dict={}
for row in resp:
    
    if not log_data.get(row['run_id'],False):
        log_data.update({row['run_id']:[]})
    log_data[row['run_id']].append(row)


# Step 1: Analyze each individual run
individual_run_reports = analyze_instagram_logs_no_pandas(log_data)

# Print individual run reports
print("--- Individual Run Reports ---")
for run_id, report in individual_run_reports.items():
    print(f"--- Report for Run ID: {run_id} ---")
    print(f"  Total Run Time (Instance): {report['total_run_time_of_this_instance']}")
    print(f"  Bot Used: {report['bot_username']}")
    print(f"  Exception: {report['exception']}")
    if report["specific_exception_reason"] != "N/A":
        print(f"  Specific Exception Reason: {report['specific_exception_reason']}")
    print(f"  Last Log Details: {report['last_log_details']}")
    print(f"  Task Completion Status for this Run: {report['task_completion_status']}")
    if report["scraped_data_summary"]:
        print(f"  Scraped Data Summary: {report['scraped_data_summary']}")
    print(f"  Found Next Page Info Count: {report['found_next_page_info_count']}")
    print(f"  Next Page Info Not Found Count: {report['next_page_info_not_found_count']}")
    print(f"  Saved File Count: {report['saved_file_count']}")
    print(f"  Downloaded File Count: {report['downloaded_file_count']}")
    if report["error_details"]:
        print("  Non-Fatal Error Details:")
        for error in report["error_details"]:
            print(f"    - Message: {error['message']}, Module/Function: {error['module_function']}, Datetime: {error['datetime']}")
    print("-" * 40)

# Step 2: Analyze the overall task status
overall_task_report = analyze_overall_task_status(individual_run_reports)

# Print overall task status
print("\n--- Overall Task Status ---")
print(f"Overall Task Status: {overall_task_report['overall_task_status']}")
print(f"Total Task Runtime: {overall_task_report['total_task_runtime']}")
print(f"Number of Runs Initiated: {overall_task_report['number_of_runs_initiated']}")
print(f"Completed Runs: {overall_task_report['completed_runs_count']}")
print(f"Failed Runs (with exception): {overall_task_report['failed_runs_count']}")
print(f"Incomplete Runs (stopped without completion log): {overall_task_report['incomplete_runs_count']}")
print("Overall Scraped Data Total:")
if isinstance(overall_task_report['overall_scraped_data_total'], dict):
    for key, value in overall_task_report['overall_scraped_data_total'].items():
        print(f"  - {key.replace('_', ' ').title()}: {value}")
else:
    print(f"  {overall_task_report['overall_scraped_data_total']}")
print(f"Overall Found Next Page Info Count: {overall_task_report['overall_found_next_page_info_count']}")
print(f"Overall Next Page Info Not Found Count: {overall_task_report['overall_next_page_info_not_found_count']}")
print(f"Overall Saved File Count: {overall_task_report['overall_saved_file_count']}")
print(f"Overall Downloaded File Count: {overall_task_report['overall_downloaded_file_count']}")
print("Overall Non-Fatal Errors Summary:")
if isinstance(overall_task_report['overall_errors_summary'], list) and overall_task_report['overall_errors_summary']:
    for error in overall_task_report['overall_errors_summary']:
        print(f"  - Message: {error['message']}, Module/Function: {error['module_function']}, Datetime: {error['datetime']}")
else:
    print(f"  {overall_task_report['overall_errors_summary']}")
print("Exceptions Summary:")
if isinstance(overall_task_report['exceptions_summary'], list) and overall_task_report['exceptions_summary']:
    for exc in overall_task_report['exceptions_summary']:
        print(f"  - Type: {exc.get('type', 'N/A')}, Name: {exc.get('name', 'N/A')}, Message: {exc.get('message', 'N/A')}")
else:
    print(f"  {overall_task_report['exceptions_summary']}")
print("Specific Exception Reasons (Overall):")
if isinstance(overall_task_report['specific_exception_reasons_overall'], list) and overall_task_report['specific_exception_reasons_overall']:
    for reason in set(overall_task_report['specific_exception_reasons_overall']):
        print(f"  - {reason}")
else:
    print(f"  {overall_task_report['specific_exception_reasons_overall']}")
print(f"Last Status of Task: {overall_task_report['last_status_of_task_run']}")
print("-" * 40)


resp=format_report_for_json_output(overall_report=overall_task_report)
s.push_data_frame_to_google_sheet(data=[resp],**{'spreadsheet_url':'https://docs.google.com/spreadsheets/d/1M9gqDNvQxU3q-BL4PL5kLIDReHzfMAOVULk8DD_KPkA/edit?gid=1674101509#gid=1674101509','worksheet_name':'scraper_report'}) """