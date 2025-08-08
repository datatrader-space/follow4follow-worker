// TOGGLE SIDEBAR
const menuBar = document.querySelector("#content nav .bx.bx-menu");
const sidebar = document.getElementById("sidebar");

menuBar.addEventListener("click", function () {
	sidebar.classList.toggle("hide");
});

const searchButton = document.querySelector(
	"#content nav form .form-input button"
);
const searchButtonIcon = document.querySelector(
	"#content nav form .form-input button .bx"
);
const searchForm = document.querySelector("#content nav form");

searchButton.addEventListener("click", function (e) {
	if (window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle("show");
		if (searchForm.classList.contains("show")) {
			searchButtonIcon.classList.replace("bx-search", "bx-x");
		} else {
			searchButtonIcon.classList.replace("bx-x", "bx-search");
		}
	}
});

function openPopup(popupId) {
	var popup = document.getElementById(popupId);
	if (popup) {
		popup.style.display = "block";
	}
}

function closePopup(popupId) {
	var popup = document.getElementById(popupId);
	if (popup) {
		popup.style.display = "none";
	}
}

function applyColumnSelection() {
	var table = document.getElementById('myTable');
	var checkboxes = document.querySelectorAll('#columnModal input[type="checkbox"]');

	checkboxes.forEach(function (checkbox) {
		var columnName = checkbox.getAttribute('data-column');
		var columnIndex = Array.from(table.rows[0].cells).findIndex(cell => cell.getAttribute('data-column') === columnName);

		if (columnIndex !== -1) {
			if (checkbox.checked) {
				table.rows[0].cells[columnIndex].style.display = '';
				Array.from(table.rows).forEach(row => row.cells[columnIndex].style.display = '');
			} else {
				table.rows[0].cells[columnIndex].style.display = 'none';
				Array.from(table.rows).forEach(row => row.cells[columnIndex].style.display = 'none');
			}
		}
	});
	document.getElementById('columnModal').style.display = 'none';
}

function toggleColumnSelection() {
	var modal = document.getElementById('columnModal');
	modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
}

document.addEventListener("DOMContentLoaded", function () {
	var uploadProxiesButton = document.querySelector(".generate-report-btn");
	var addProxiesPopup = document.getElementById("addProxiesPopup");

	uploadProxiesButton.addEventListener("click", function () {
		openPopup("addProxiesPopup");
	});
});

if (window.innerWidth < 768) {
	sidebar.classList.add("hide");
} else if (window.innerWidth > 576) {
	searchButtonIcon.classList.replace("bx-x", "bx-search");
	searchForm.classList.remove("show");
}

window.addEventListener("resize", function () {
	if (this.innerWidth > 576) {
		searchButtonIcon.classList.replace("bx-x", "bx-search");
		searchForm.classList.remove("show");
	}
});

function applyFilter() {
	var serialNumberFilter = document.getElementById('serial-number-filter').value.toLowerCase();
	var stateFilter = document.getElementById('state-filter').value.toLowerCase();

	var rows = document.querySelectorAll('.proxy-row');

	rows.forEach(function (row) {
		var serialNumber = row.children[1].innerText.toLowerCase();
		var state = row.children[2].innerText.toLowerCase();

		if (serialNumber.includes(serialNumberFilter) && (stateFilter === '' || state === stateFilter)) {
			row.style.display = '';
		} else {
			row.style.display = 'none';
		}
	});
}


function toggleLeftSidebar() {
	var sidebar = document.getElementById('sidebar');
	sidebar.classList.toggle('hide');
	updateHoverState();
}

function updateHoverState() {
	var icons = document.querySelectorAll('#sidebar i');
	var sidebar = document.getElementById('sidebar');

	icons.forEach(function (icon) {
		if (sidebar.classList.contains('hide')) {
			icon.classList.add('no-hover');
		} else {
			icon.classList.remove('no-hover');
		}
	});
}

function saveApiKey() {
	var apiKey = document.getElementById('smspvaApiKey').value;
	alert('API key saved: ' + apiKey);
}

var csrftoken = getCookie('csrftoken');
$.ajax({
	type: 'POST',
	beforeSend: function (xhr, settings) {
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
	},
});

function goToPage(pageNumber) {
	window.location.href = '?page=' + pageNumber;
}

function applyFilters() {
	var typeFilter = document.getElementById('type-filter').value.toLowerCase();
	var statusFilter = document.getElementById('status-filter').value.toLowerCase();
	var rows = document.querySelectorAll('.proxy-row');

	rows.forEach(function (row) {
		var type = row.cells[3].textContent.toLowerCase();
		var status = row.cells[5].textContent.toLowerCase();

		if ((type.includes(typeFilter) || typeFilter === '') && (status.includes(statusFilter) || statusFilter === '')) {
			row.style.display = '';
		} else {
			row.style.display = 'none';
		}
	});
};

var addServerUrl = "{% url 'add_server' %}";

function sendFormData() {
	var formData = {
		'instance_id': document.getElementById('instance_id').value,
		'server_name': document.getElementById('server_name').value,
		'load': document.getElementById('load').value,
		'last_beat': document.getElementById('last_beat').value,
		'tags': document.getElementById('tags').value,
		'csrfmiddlewaretoken': '{{ csrf_token }}'
	};

	console.log(formData);

	var xhr = new XMLHttpRequest();
	xhr.open("POST", addServerUrl, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.setRequestHeader("X-CSRFToken", formData.csrfmiddlewaretoken);

	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
				// Successful response
				console.log(xhr.responseText);
			} else {
				// Handle errors
				console.error('Error:', xhr.status, xhr.statusText);
			}
		}
	};

	xhr.send(JSON.stringify(formData));
}

var tabs = $('.tabs');
var selector = $('.tabs').find('a').length;
//var selector = $(".tabs").find(".selector");
var activeItem = tabs.find('.active');
var activeWidth = activeItem.innerWidth();
$(".selector").css({
  "left": activeItem.position.left + "px", 
  "width": activeWidth + "px"
});

$(".tabs").on("click","a",function(e){
  e.preventDefault();
  $('.tabs a').removeClass("active");
  $(this).addClass('active');
  var activeWidth = $(this).innerWidth();
  var itemPos = $(this).position();
  $(".selector").css({
    "left":itemPos.left + "px", 
    "width": activeWidth + "px"
  });
});

function openPoppyUp() {
	document.getElementById('poppy-up').style.display = 'block';
}

function closePoppyUp() {
	document.getElementById('poppy-up').style.display = 'none';
}

function openManageProxiesPopUp() {
	openPopup('manage-proxies-pop-up');
}

function closeManageProxiesPopUp() {
    closeAllPopups();
}

function openManageAccPopUp() {
	openPopup('manage-acc-pop-up');
}

function closeManageAccPopUp() {
	closeAllPopups();
}

function openManageListPopUp() {
	openPopup('manage-list-pop-up');
}

function closeManageListPopUp() {
	closeAllPopups();
}

function openManageTasksPopUp() {
	openPopup('manage-tasks-pop-up');
}

function closeManageTasksPopUp() {
	closeAllPopups();
}

function openManageDevicePopUp() {
	openPopup('manage-device-pop-up');
}

function closeManageDevicePopUp() {
	closeAllPopups();
}

function openSchedulerPopUp() {
	openPopup('manage-scheduler-pop-up');
}

function closeSchedulerPopUp() {
	closeAllPopups();
}

function openPostSettingsPopUp() {
	openPopup('manage-post-settings-pop-up');
}

function closePostSettingsPopUp() {
	closeAllPopups();
}

function openScrapeSettingsPopUp() {
	openPopup('manage-scrape-settings-pop-up');
}

function closeScrapeSettingsPopUp() {
	closeAllPopups();
}

function openFollowSettingsPopUp() {
	openPopup('manage-follow-settings-pop-up');
}

function closeFollowSettingsPopUp() {
	closeAllPopups();
}

function openUnfollowSettingsPopUp() {
	openPopup('manage-unfollow-settings-pop-up');
}

function closeUnfollowSettingsPopUp() {
	closeAllPopups();
}

function openDMSettingsPopUp() {
	openPopup('manage-dm-settings-pop-up');
}

function closeDMSettingsPopUp() {
	closeAllPopups();
}

function openDVSettingsPopUp() {
	openPopup('manage-dv-settings-pop-up');
}

function closeDVSettingsPopUp() {
	closeAllPopups();
}

function openRepostSettingsPopUp() {
	openPopup('manage-repost-settings-pop-up');
}

function closeRepostSettingsPopUp() {
	closeAllPopups();
}

function openShareSettingsPopUp() {
	openPopup('manage-share-settings-pop-up');
}

function closeShareSettingsPopUp() {
	closeAllPopups();
}

function openFavoriteSettingsPopUp() {
	openPopup('manage-favorite-settings-pop-up');
}

function closeFavoriteSettingsPopUp() {
	closeAllPopups();
}

function openCommentSettingsPopUp() {
	openPopup('manage-comment-settings-pop-up');
}

function closeCommentSettingsPopUp() {
	closeAllPopups();
}

function openPopup(popupId) {
	closeAllPopups();
	document.getElementById(popupId).style.display = "block";
}

function closeAllPopups() {
	var popups = document.getElementsByClassName("poppy-up-content");
	for (var i = 0; i < popups.length; i++) {
		popups[i].style.display = "none";
	}
}