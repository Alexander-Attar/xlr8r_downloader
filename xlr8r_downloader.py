# Alexander Attar - Summer 2013
# Update: Vladimir Bakalov - Spring 2015

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import random
import urllib2
import re
from os.path import expanduser
from bs4 import BeautifulSoup as bs


def randomize_user_agent():
    """ Generates a random user_agent for a request header """

    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)'
    ]

    return {'User-Agent': random.choice(user_agents)}


def main():
    """
    xlr8r_downloader.py
        Downloads free music from the latest 10 pages of xlr8r.com
        and saves them to the Downloads directory on OSX.
        * Note: 10 pages of downloads equals about 70 tracks
          dating back to about a month of posts.

    Usage:
        python xlr8r_downloader.py
    """

    home = expanduser("~")  # setup a path to the OSX ~/ directory
    download_directory = "/Music/"

    try:  # to download music
        page = 1
        while page < 10:  # Download all tracks from the lastest 3 pages at xlr8r.com
            page_url = 'http://www.xlr8r.com/mp3/page/%s/' % page
            request = urllib2.Request(page_url, None, randomize_user_agent())
            html = urllib2.urlopen(request)
            soup = bs(html)

            for link in soup.findAll("a", {"class":"vw-read-more"}):
		page_url1 = link['href']
		print "Opening: %s" % (page_url1)
		request1 = urllib2.Request(page_url1, None, randomize_user_agent())
            	html1 = urllib2.urlopen(request1)
            	soup1 = bs(html1)
		
		for link1 in soup1.findAll("a", href=re.compile("\.mp3")):
		    url1 = link1['href']
		    print "Fetching: %s" % (url1)

                    # the file name contains the path to the OSX ~/Downloads directory
                    file_name = urllib2.unquote(url1.split('/')[-1])  # decode the url string
                    file_location = download_directory + file_name
                    u = urllib2.urlopen(url1)
                    f = open(file_location, 'wb')
                    meta = u.info()
                    file_size = int(meta.getheaders("Content-Length")[0])
                    print "Downloading: %s Bytes: %s" % (file_name, file_size)  # status bar

                    file_size_dl = 0
                    block_sz = 8192
                    while True:
                        buffer = u.read(block_sz)
                    	if not buffer:
                            break

                        file_size_dl += len(buffer)
                        f.write(buffer)
                        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                        status = status + chr(8)*(len(status)+1)
                        print status,

                    f.close()

            page += 1

        print "Downloading complete!"

    except Exception as e:
        print 'Unable to save mp3: %s' % str(e)

if __name__ == '__main__':
    main()
