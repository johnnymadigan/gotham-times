# -----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no:    nXXXXXXXX
#    Student name:  Johnny Madigan
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
# --------------------------------------------------------------------#


# -----Assignment Description-----------------------------------------#
#
#  News Feed Aggregator
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application that allows the user to aggregate RSS news feeds.
#  See the instruction sheet accompanying this file for full details.
#
# --------------------------------------------------------------------#


# -----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.
#
# NB: You may NOT use any Python modules that need to be downloaded
# and installed separately, such as "Beautiful Soup" or "Pillow".
# Only modules that are part of a standard Python 3 installation may
# be used.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
# from urllib.request import urlopen
from urllib import request # 2021 fix -J

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.  You may import other widgets
# from the Tkinter module provided they are ones that come bundled
# with a standard Python 3 implementation and don't have to
# be downloaded and installed separately.)
from tkinter import *

# Import a special Tkinter widget we used in our demo
# solution.  (You do NOT need to use this particular widget
# in your solution.  You may import other such widgets from the
# Tkinter module provided they are ones that come bundled
# with a standard Python 3 implementation and don't have to
# be downloaded and installed separately.)
from tkinter.scrolledtext import ScrolledText

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

import re # 2021 fix -J

# Import the standard SQLite functions (just in case they're
# needed one day).
from sqlite3 import *

#
# --------------------------------------------------------------------#


# -----------------------------------------------------------
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document or RSS Feed.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will hide its identity
#      from the web server. This can be used to prevent the
#      server from blocking access to Python programs. However
#      we do NOT encourage using this option as it is both
#      unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = False,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = True):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
# --------------------------------------------------------------------#


# -----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# Name of the exported news file. To simplify marking, your program
# should produce its results using this file name.
news_file_name = 'news.html'





# SETUP
#_________________________________________
    # Sets up the initial window
news_aggregator = Tk()
news_aggregator.title("The Gotham Times")
news_aggregator.configure(background='white')
import sqlite3




# HEADING & LOGO
#_________________________________________
    # Heading
heading = Label(news_aggregator, text="THE GOTHAM TIMES",
              bg='white', fg='black', font=('Arial 25 bold italic'))
heading.grid(row=0, column=1, columnspan=4, pady=5, padx=10)


    # Logo
logo_image = PhotoImage(file="batman_rss.png")
logo = Label(news_aggregator, image=logo_image, bg='white')
logo.grid(row=0, rowspan=5, column=5, pady=5, padx=10)


    # Credits
creds = Label(news_aggregator, text="Johnny Madigan", bg='white',
              fg='lightgrey', font=('Arial 8'))
creds.grid(row=5, column=5, pady=10)





# SUB-HEADINGS
#_________________________________________
    # Sub-heading
feed_heading = Label(news_aggregator, text=" NEWS FEEDS: ",
              bg='whitesmoke', fg='grey', relief=GROOVE,
                     font=('Arial 10 bold italic'))
feed_heading.grid(row=1, column=2, columnspan=2, pady=10)


    # Adds 'LIVE' symbols
live_image = PhotoImage(file="live.png")
live1 = Label(news_aggregator, image=live_image, bg='white')
live1.grid(row=3, column=1, pady=10)
live2 = Label(news_aggregator, image=live_image, bg='white')
live2.grid(row=3, column=2, pady=10)


    # Adds 'ARCHIVED' headings
archive1 = Label(news_aggregator, text="ARCHIVED", bg='white',
                 fg='darkorange', font=('Arial 8'))
archive1.grid(row=3, column=3, pady=10)
archive2 = Label(news_aggregator, text="ARCHIVED", bg='white',
                 fg='darkorange', font=('Arial 8'))
archive2.grid(row=3, column=4, pady=10)





# NEWS FEEDS HEADINGS
#_________________________________________
    # 'LA Times' heading
feed1 = Label(news_aggregator, text=" LA Times ",
              bg='whitesmoke', fg='black', relief=GROOVE,
              font=('Arial 10 italic'))
feed1.grid(row=2, column=1, pady=(10, 5), padx=(10, 2.5))


    # 'NineNews' heading
feed2 = Label(news_aggregator, text=" 9News ",
              bg='whitesmoke', fg='black', relief=GROOVE,
              font=('Arial 10 italic'))
feed2.grid(row=2, column=2, pady=(10, 5), padx=2.5)


    # 'New York Post' heading
feed3 = Label(news_aggregator, text=" New York Post ",
              bg='whitesmoke', fg='black', relief=GROOVE,
              font=('Arial 10 italic'))
feed3.grid(row=2, column=3, pady=(10, 5), padx=2.5)


    # 'HuffPosst' heading
feed4 = Label(news_aggregator, text=" HuffPost ",
              bg='whitesmoke', fg='black', relief=GROOVE,
              font=('Arial 10 italic'))
feed4.grid(row=2, column=4, pady=(10, 5), padx=(2.5, 10))





# PREVIEW LISTBOX
#_________________________________________
    # Sets up the preview box
    # With a scrollbar & placeholder text
preview = ScrolledText(news_aggregator, width=50, height=25, wrap=WORD)
preview.grid(row=6, column=1, columnspan=4, pady=10, padx=10)
preview.config(fg='grey', font=('Arial 10'))
preview.insert(INSERT, '\n       Preview your custom feed here!')
preview.config(state='disabled')





# DOWNLOADING THE LIVE FEEDS
#_________________________________________
    # Downloads 'LA Times' LIVE
latimes_live = download('https://www.latimes.com/environment/rss2.0.xml')


    # Downloads '9News LIVE'
ninenews_live = download('https://www.9news.com.au/rss')





# IMPORTING ARCHIVED FEEDS
#_________________________________________
    # Imports 'New York Post' archived file
with open('2.10.2019_newyorkpost.xhtml', encoding='utf-8') as f:
    newyorkpost_xml = f.read()


    # Imports 'HuffPost' archived file
with open('27.09.2019_huffpost.xhtml', encoding='utf-8') as f:
    huffpost_xml = f.read()





# SCANS ALL FEED XMLs/HTMLs FOR ELEMENTS
# USING PATTERN MATCHING (REGULAR EXPRESSIONS)
#_________________________________________
def regular_expressions(position, string, source, update):
    # Divides XML/HTML into sections (isolating stories)
    html_code = re.findall(r'<item>(.*?)</item>',
                                 str(string), flags=DOTALL)
    isolated_story = html_code[int(position)]


    # From the story, the headline is found
    headline_element = re.findall(r'<title>(.*?)</title>',
                                  str(isolated_story))
    headline = headline_element[0]
    fixed_headline = headline.replace("&#39;", "").replace("&#x27;", "")\
                     .replace("&#8217;", "").replace("&#8216;", "").replace("'", "")


    # The corresponding news source is added
    news_source = source


    # From the story, the date/time is found
    pubdate_element = re.findall(r'<pubDate>(.*?)</pubDate>',
                                 str(isolated_story))
    pubdate = pubdate_element[0]


    # Elements are combined into one string
    preview_string = ('"' + fixed_headline + '" [' + news_source + ' - '
                      + pubdate + "]\n\n")


    # IF preview is selected for updating, then...
    if update == 'prev':
        preview.insert(INSERT, preview_string)


    # IF database is selected for updating then...
    elif update == 'database':
        con = sqlite3.connect('news_log.db')
        cur = con.cursor()
        cur.execute("INSERT INTO selected_stories VALUES('" + fixed_headline +
                    "', '" + news_source + "', '" + pubdate + "')")
        con.commit()





# UPDATES THE PREVIEW USING BUTTONS
#_________________________________________
def update_preview(amount):


    # Allows changes to the preview box
    preview.config(state='normal')


    # Clears the preview box
    preview.delete(0.0, END)


    # Checks all button's values
    feed1_value = feed1_b.get()
    feed2_value = feed2_b.get()
    feed3_value = feed3_b.get()
    feed4_value = feed4_b.get()


    # Generates 'LA Times' stories
    for stories in range(0, feed1_value):
        regular_expressions(stories, latimes_live, 'LA Times', 'prev')

    # Generates '9News' stories
    for stories in range(0, feed2_value):
        regular_expressions(stories, ninenews_live, '9News', 'prev')

    # Generates 'New York Post' stories
    for stories in range(0, feed3_value):
        regular_expressions(stories, newyorkpost_xml, 'New York Post', 'prev')

    # Generates 'HuffPost' stories
    for stories in range(0, feed4_value):
        regular_expressions(stories, huffpost_xml, 'HuffPost', 'prev')


    # If all button's are set to 0...
    # No stories are displayed and...
    # the placeholder text returns
    if feed1_value == 0 and feed2_value == 0 and \
       feed3_value == 0 and feed4_value == 0:
        preview.insert(INSERT, '\n       Preview your custom feed here!')


    # Locks the preview box
    preview.config(state='disabled')





# BUTTONS FOR STORY SELECTION
#_________________________________________
    # 'NY Times' scale button
feed1_b = Scale(news_aggregator, from_=0,to=10, orient=HORIZONTAL,
                command=update_preview)
feed1_b.grid(row=4, column=1, pady=5, padx=(10, 2.5))


    # '9News' scale button
feed2_b = Scale(news_aggregator, from_=0,to=10, orient=HORIZONTAL,
                command=update_preview)
feed2_b.grid(row=4, column=2, pady=5, padx=2.5)


    # 'New York Post' scale button
feed3_b = Scale(news_aggregator, from_=0,to=10, orient=HORIZONTAL,
                command=update_preview)
feed3_b.grid(row=4, column=3, pady=5, padx=2.5)


    # 'HuffPost' scale button
feed4_b = Scale(news_aggregator, from_=0,to=10, orient=HORIZONTAL,
                command=update_preview)
feed4_b.grid(row=4, column=4, pady=5, padx=(2.5, 10))





# TEMPLATE FOR THE EXPORTED HTML
#_________________________________________
# Beginning of the HTML template with styles, logo, etc
html_template_open = """<!DOCTYPE html>
<html>
    <head>

        <!-- Unicode chars-->
    	<meta charset = 'UTF-8'>

        <!-- Defines the title for the window/tab -->
    	<title>
        The Gotham Times
        </title>

        <!-- Sets the styles for each tag -->
        <style>
        body {
        background-image: url(https://s3.amazonaws.com/media.eremedia.com/wp-content/uploads/2018/10/23114015/batman.jpg);
        height: 100%;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: fixed;
        }
        table, th, td {
        border-collapse: collapse;
        width: 600px;
        border-top: 3px double grey;
    	border-left: 0px solid;
    	border-right: 0px solid;
        background: white;
        table-layout: fixed;
        margin-left:auto; 
    	margin-right:auto;
    	padding: 10px;
        }
        img {
        width:500px;
        height: auto;
    	display:block;
    	margin-left: auto;
        margin-right: auto;
        user-select: none;
        }
        h1 {
        text-align: center;
        font-size:55px;
        user-select: none;
        }
        h2 {
        text-align: left;
        font-family: Arial;
        padding-left:50px;
        padding-right:50px;
        user-select: none;
        }
        p {
        padding-left:50px;
        padding-right:50px;
        text-align: justify;
        text-justify: inter-word;
        user-select: none;
        }
        div {
        text-align: center;
        user-select: none;
        }
        li {
        list-style-type: circle;
        padding-left:50px;
        padding-right:50px;
        }
        </style>
    </head>
<body>

    <!-- Creates a single column for the custom feed -->
    <table>
    
        <tr>
            <td>

            <!-- Main heading -->
            <h1>THE GOTHAM TIMES </h1>

            <!-- Credits -->
            <p><div><sup>Johnny Madigan</sup></div></p>
            </td>
        </tr>

        <tr>
            <td>

            <!-- Main splash image -->
            <img src="http://4.bp.blogspot.com/_2kjisMm3M9Y/SFUY_svmSUI/AAAAAAAAD4U/Lvs3PO7Jap8/s400/the+gotham+times+volume+3.jpg" alt="The Gotham Times Logo">
            </td>
        </tr>



<!-- CUSTOM FEED IS INSERTED BELOW -->



"""


# Closing of the HTML template including hyperlinks to original sources
html_template_close = """

<!-- WRAPPING UP THE HTML DOCUMENT -->



        <tr>
    	    <td>

            <!-- Heading for sources -->
    	    <h2>ORIGINAL FEEDS</h2>

            <!-- List of external links -->
    	    <li><a href="https://www.latimes.com/environment" target="_blank">LA Times: Environment</a></li>
    	    <li><a href="https://www.9news.com.au" target="_blank">9News: Latest</a></li>
    	    <li><a href="https://nypost.com/entertainment/" target="_blank">New York Post: Entertainment</a></li>
            <li><a href="https://www.huffpost.com/news/crime" target="_blank">HuffPost: Crime</a></li><br>
            </td>
        </tr>
        
    </table>
</body>
</html>
"""





# SCANS ALL FEED XMLs/HTMLs FOR ELEMENTS
# USING PATTERN MATCHING (REGULAR EXPRESSIONS)
#_________________________________________
def html_elements(position, string, source):
    # Divides XML/HTML into sections (isolating stories)
    html_code = re.findall(r'<item>(.*?)</item>',
                                 str(string), flags=DOTALL)
    isolated_story = html_code[int(position)]


    # From the story, the headline is found
    headline_element = re.findall(r'<title>(.*?)</title>',
                                  str(isolated_story))
    headline = headline_element[0]
    fixed_headline = headline.replace("&#39;", "'").replace("&#x27;", "'")\
                     .replace("&#8217;", "'").replace("&#8216;", "'")
        # Add heading tags
    enclosed_headline = '<h2>' + fixed_headline + '</h2>'


    # From the story, the image is found
    img_element = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 str(isolated_story))
    img = str(img_element[-1])
    fixed_img = img.replace("['","").replace("']", "")
        # Embed in image tag
    enclosed_img = '<img src="' + fixed_img + '">'


    # From the story, the description is found
    desc_element = re.findall(r'<description>(.*?)</description>',
                                 str(isolated_story))
    desc = desc_element[0]
    fixed_desc = desc.replace("]]>", "").replace("<![CDATA[", "")\
                 .replace("<p>", "").replace("</p>", "")
        # Add paragraph tags
    enclosed_desc = '<p>' + fixed_desc + '</p>'


    # From the story, the date/time is found
    pubdate_element = re.findall(r'<pubDate>(.*?)</pubDate>',
                                 str(isolated_story))
    pubdate = pubdate_element[0]
        # Add paragraph tags
        # Add news source
    enclosed_pubdate = '<p>' + source + ' - ' + pubdate + '</p>'


    # All elements are combined to form a segment of HTML code
    # This code generates a single story in proper formatting
    final_story_code = ("<tr>\n<td>\n" + enclosed_headline + "\n\n" + enclosed_img
                        + "\n\n" + enclosed_desc + "\n\n" + enclosed_pubdate
                        + "\n</td>\n</tr>\n\n")


    # The string for the story is returned
    return final_story_code





# EXPORTS PREVIEW AS AN HTML
# AFTER GENERATING FINAL CODE
#_________________________________________
def generate_html():


    # Checks all button's values
    feed1_value = feed1_b.get()
    feed2_value = feed2_b.get()
    feed3_value = feed3_b.get()
    feed4_value = feed4_b.get()


    # Opens the HTML file ready for editing
    html_file = open(news_file_name, 'w', encoding='UTF-8')


    # Empty lists for html code to be inserted chronologically
    LA_Times_stories = []
    NineNews_stories = []
    New_York_Post_stories = []
    HuffPost_stories = []


    # Creates html code for each story using a regular expression function
    # Inserting stories into their corresponding list above
    for stories in range(0, feed1_value):
            result = html_elements(stories, latimes_live, 'LA Times')
            LA_Times_stories.append(result)

    for stories in range(0, feed2_value):
            result = html_elements(stories, ninenews_live, '9News')
            NineNews_stories.append(result)

    for stories in range(0, feed3_value):
            result = html_elements(stories, newyorkpost_xml, 'New York Post')
            New_York_Post_stories.append(result)

    for stories in range(0, feed4_value):
            result = html_elements(stories, huffpost_xml, 'HuffPost')
            HuffPost_stories.append(result)


    # Lists become strings ready to be inserted into the html template string
    LA_Times_list_to_string = ' '.join(LA_Times_stories)
    NineNews_list_to_string = ' '.join(NineNews_stories)
    New_York_Post_list_to_string = ' '.join(New_York_Post_stories)
    HuffPost_list_to_string = ' '.join(HuffPost_stories)


    # All story strings above are inserted between the HTML opening template
    # and the HTML closing template to form one giant string...
    # Ready to be exported!
    final_html = (html_template_open + LA_Times_list_to_string + NineNews_list_to_string
                  + New_York_Post_list_to_string + HuffPost_list_to_string + html_template_close)
    html_file.write(final_html)
    html_file.close()





# EXPORT BUTTON
#_________________________________________
export = Button(news_aggregator, text='Export selections', font=('Arial 10'),
                bg='lightgrey', fg='grey', width=20, command=generate_html)
export.grid(row=8, column=2, columnspan=2, pady=(10,0), padx=10)





# CLEAR & UPDATE DATABASE
#_________________________________________
def clear_and_update():


    # Connects to database
    con = sqlite3.connect('news_log.db')


    # Clears the database to start fresh
    cur = con.cursor()
    cur.execute("""DELETE FROM selected_stories""")
    con.commit()
    cur.close()
    con.close()


    # Checks all button's values
    feed1_value = feed1_b.get()
    feed2_value = feed2_b.get()
    feed3_value = feed3_b.get()
    feed4_value = feed4_b.get()


    # Inserts 'LA Times' stories into DB
    for stories in range(0, feed1_value):
        regular_expressions(stories, latimes_live, 'LA Times', 'database')

    # Inserts '9News' stories into DB
    for stories in range(0, feed2_value):
        regular_expressions(stories, ninenews_live, '9News', 'database')

    # Inserts 'New York Post' stories into DB
    for stories in range(0, feed3_value):
        regular_expressions(stories, newyorkpost_xml, 'New York Post', 'database')

    # Inserts 'HuffPost' stories into DB
    for stories in range(0, feed4_value):
        regular_expressions(stories, huffpost_xml, 'HuffPost', 'database')





# SAVE TO DATABASE BUTTON
#_________________________________________
save = Button(news_aggregator, text='Save selections', font=('Arial 10'),
                bg='lightgrey', fg='grey', width=20, command=clear_and_update)
save.grid(row=9, column=2, columnspan=2, pady=(0,20), padx=10)





# END OF SUBMISSION
#_________________________________________
news_aggregator.mainloop()
