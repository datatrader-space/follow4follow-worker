from urllib.parse import urlparse,urldefrag
class Extractors():
    pass


class SeoExtractors(Extractors):
    def extract_domain_from_url(self,url):
        parsed_url=urlparse(url)
        domain=parsed_url.netloc
        domain
        return domain.replace('.','_')
    def defrage_url(self,url):
        return urldefrag(url)
    def create_identifier_from_url(self,url):
       
        parsed_url =urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/")
        filename = ";".join(path_parts)
        filename = filename # Limit filename length to 255 characters
        filename = filename.replace("?", "!Q").replace("&", "!A").replace("=", "!E")
        return filename 
    def convert_identifier_to_url(self,filename):
        url_path = filename[:-4].replace(";.", "/").replace("!Q", "?").replace("!A", "&").replace("!E", "=")
    def group_url_by_domain(self,urls):

        grouped_urls = {}
    
        for url in urls:
            if type(url)==float:
                continue
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            url_without_fragment = urldefrag(url).url  # Remove fragment from URL
            
            if domain in grouped_urls and url_without_fragment in grouped_urls[domain]:
                continue  # Skip adding duplicate URL
            else:
                if domain in grouped_urls:
                    grouped_urls[domain].append(url_without_fragment)
                else:
                    grouped_urls[domain] = [url_without_fragment]
    

        
        return grouped_urls

class KeywordExtractor(Extractors):

    def basic_keyword_extractor(self,text, num_keywords=None):
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        from collections import Counter
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens if word.isalpha()]
        filtered_tokens = [word for word in tokens if word not in stopwords.words('english')]
        keyword_counter = Counter(filtered_tokens)
        resp=keyword_counter.most_common(num_keywords)
        return resp