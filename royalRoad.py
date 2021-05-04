import requests
import json

def royalRoadChapters(text):
    beg=text.find("tbody")+7
    end=text[beg:].find("</tbody")
    tot=text[beg:][:end]
    items=tot.split("</tr>")
    del items[len(items)-1]
    chapters=[]
    for index in range(len(items)):
        i = items[index]
        link=i[i.find('data-url="')+10:]
        link=link[:link.find('"')]
        name=i[i.find('<a')+10:]
        name=name[name.find('>')+1:name.find('<')].strip()
        chapters.append({'ext': link, 'chapter name': name, 'chapter number': index})
    return chapters

def royalRoadBookInfo(bookLink):
    res = requests.get(bookLink)
    text=res.text
    bookName=text[text.find('title" content="')+16:][:text[text.find('title" content="')+16:].find('"')]
    chapters = royalRoadChapters(text)
    book={}
    book["link"] = bookLink
    book["name"] = bookName
    book["website"] = "royalroad"
    book["chapters"] = chapters
    book["number of chapters"] = len(chapters)
    return book

def NewBook(bookLinkName, bookLink):
    if (bookLink.find("royalroad")!=-1):
        book=royalRoadBookInfo(bookLink)
    with open(bookLinkName+'.json', 'w') as f:
        print(json.dumps(book, indent=4), file=f)
    return book

#it is assumed that the book is already saved and needs an update
def UpdateBook(bookLinkName, bookLink):
    f=open(bookLinkName+'.json', 'r')
    savedChapters = json.loads(f.read())['chapters']
    res = requests.get(bookLink)
    text=res.text
    onlineChapters = royalRoadChapters(text)
    for i in range(min([len(savedChapters),len(onlineChapters)])):
        if (savedChapters[i] != onlineChapters[i]):
            print(onlineChapters[i])
    if (len(savedChapters) < len(onlineChapters)):
        print(onlineChapters[len(savedChapters):])
    if (len(savedChapters) > len(onlineChapters)):
        print(savedChapters[len(onlineChapters):])
    NewBook(bookLinkName, bookLink)

# NewBook("discovering-magic", "https://www.royalroad.com/fiction/26899/discovering-magic")
# NewBook("silvergates-northworld", "https://www.royalroad.com/fiction/26157/silvergates-northworld-book-1-complete")
UpdateBook("discovering-magic", "https://www.royalroad.com/fiction/26899/discovering-magic")
