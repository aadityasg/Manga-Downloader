import urllib
import sys

def index_finder(any_url):
    any_url_page=urllib.urlopen(any_url).read()
    index_link_start=24+any_url_page.find('<h2 class="c2"><a href="')
    any_url_page=any_url_page[index_link_start:]
    index_link_end=any_url_page.find('"')
    index_url="http://mangareader.net"+any_url_page[:index_link_end]
    return index_url

def chapter_list_finder(index_url):
    index_data=urllib.urlopen(index_url).read()
    list_start=index_data.find('<div id="chapterlist">')
    index_data=index_data[list_start:]
    list_end=index_data.find('</table>')
    index_data=index_data[:list_end]

    chap_list=[]
    link_start=0
    while link_start!=8:
        link_start=9+index_data.find('<a href="')
        if link_start!=8:
            index_data=index_data[link_start:]
            link_end=index_data.find('"')
            link='http://www.mangareader.net'+index_data[:link_end]
            chap_list.append(link)
            index_data=index_data[link_end+1:]
    return chap_list

def chap_to_download():
    chap_download=[]

    for i in range(len(sys.argv)-1):
        k=i+1
        arg=str(sys.argv[k])
        hyphen=arg.find('-')
        if hyphen==-1:
            chap_download.append(int(arg))
        else:
            start=int(float(arg[:hyphen]))
            end=int(float(arg[hyphen+1:]))
            while start<=end:
                chap_download.append(int(start))
                start=start+1
    return chap_download

def download(chap_list,chap_download,path):
    for i in range(len(chap_download)):
        chap_url=chap_list[chap_download[i]-1]
        
        page=urllib.urlopen(chap_url).read()
        optionp=page
        k=1
        optionstart=0
        while optionstart!=-1:
            optionstart=optionp.find('<option value="')
            if optionstart!=-1:
                optionp=optionp[optionstart+15:]
                optionend=optionp.find('"')
                chapter_page='http://www.mangareader.net'+optionp[:optionend]
                name='chapter '+str(chap_download[i])+'- page '+str(k)
                print 'downloading ' + name
                #print chapter_page
                page_data=urllib.urlopen(chapter_page).read()
                page_data_copy=page_data
                links=18+page_data.find("document['pu'] = '")
                page_data=page_data[links:]
                linke=page_data.find("'")
                finalurl=page_data[:linke]
                
                if len(finalurl)==0:
                    imgholder_start=page_data_copy.find('id="imgholder"')
                    page_data_copy=page_data_copy[imgholder_start:]
                    img_src_start=page_data_copy.find('src="')+5
                    page_data_copy=page_data_copy[img_src_start:]
                    img_src_end=page_data_copy.find('"')
                    finalurl=page_data_copy[:img_src_end]
                print finalurl
                f=open(path+name+".jpg",'wb')
                f.write(urllib.urlopen(finalurl).read())
                f.close()
                k=k+1
        

any_url=raw_input("enter the URl of any page from the same MANGA : ")
path=raw_input("Enter the path for saving the manga :")
index_url=index_finder(any_url)
chap_list=chapter_list_finder(index_url)
chap_download=chap_to_download()

download(chap_list,chap_download,path)
