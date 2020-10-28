This is my very-very old project. I should rework a lot of stuff.


<hr>
<p class="has-line-data" data-line-start="1" data-line-end="2">[What it is?]</p>
<p class="has-line-data" data-line-start="3" data-line-end="6">[Web_scraper] - prototype of HTML parser which collect data from web tables.<br>
[Web_scraper] - main goal is to collect person’s data from web tables such as: ‘Full Name’, ‘Email’, ‘Gender’, ‘Highest Degree Earned’, ‘University/ School’ then [INSERT] it to PostgreSQL data base and then encrypt,<br>
then [Web_scraper] shows statistic of people with and without degree in form of pie chart.</p>
<p class="has-line-data" data-line-start="7" data-line-end="10">In file [web_scraper.py] you will see MARKS.<br>
#[!!!] - that indicates you what exactly you can change in order to setup [web_scraper.py].<br>
Mark like this - [36] shows on which line of code you can find reference</p>
<hr>
<p class="has-line-data" data-line-start="12" data-line-end="13">[First setup]</p>
<p class="has-line-data" data-line-start="14" data-line-end="17">On line [36]:<br>
conn = psycopg2.connect(“host=localhost dbname=postgres user=postgres password=admin”) #[!!!]<br>
Change host, dbname, user and password to yours from PostgreSQL</p>
<p class="has-line-data" data-line-start="18" data-line-end="21">Then on line [63]:<br>
cur.execute(&quot;INSERT INTO parser VALUES<br>
Change name “parser” to the name of [your] table in PostgreSQL</p>
<p class="has-line-data" data-line-start="22" data-line-end="25">On line [70]:<br>
cur.execute(“INSERT INTO parser VALUES (%s, %s, %s, %s, %s)”, row)<br>
change name “parser” to the name of [your] table PostgreSQL</p>
<hr>
<p class="has-line-data" data-line-start="28" data-line-end="29">[Manual how-to]</p>
<ol>
<li class="has-line-data" data-line-start="30" data-line-end="31">
<p class="has-line-data" data-line-start="30" data-line-end="31">Create Virtual environment —&gt; put files inside —&gt; pip install -r requirements.txt</p>
</li>
<li class="has-line-data" data-line-start="31" data-line-end="32">
<p class="has-line-data" data-line-start="31" data-line-end="32">Run program from terminal or PyCharm</p>
</li>
<li class="has-line-data" data-line-start="32" data-line-end="33">
<p class="has-line-data" data-line-start="32" data-line-end="33">ENTER URL TO NEEDED INTERNET PAGE from whom you want to gather data from tables.</p>
</li>
<li class="has-line-data" data-line-start="33" data-line-end="42">
<p class="has-line-data" data-line-start="33" data-line-end="34">You will be asked if you want to upload gathered data to PostgreSQL?</p>
<pre><code>             To upload files in PostgreSQL you need to change:
             Line [36] host, dbname, user, password
             You can change this values with any text editor
             in file itself [web_scraper.py]
             change word: &quot;parser&quot; to your table's name on lines [63] and [70]
</code></pre>
</li>
<li class="has-line-data" data-line-start="42" data-line-end="57">
<p class="has-line-data" data-line-start="42" data-line-end="43">You will be asked if you want to Encrypt your data. By default [password] that Ecnrypt and Decrypt is “key”</p>
<pre><code>                             To change password which will Encrypt and Decrypt values
                             change it there:
                             [64]     cur.execute(&quot;INSERT INTO parser VALUES\
                                         (PGP_SYM_ENCRYPT(%s, 'key')::text,\
                                         PGP_SYM_ENCRYPT(%s, 'key')::text,\
                                         PGP_SYM_ENCRYPT(%s, 'key')::text,\
                                         PGP_SYM_ENCRYPT(%s, 'key')::text,\
                                         PGP_SYM_ENCRYPT(%s, 'key')::text)&quot;, row)

                                 EXAMPLE: PGP_SYM_ENCRYPT(%s, 'new_key')::text,


                             [WARNING: DO NOT STORE PASSWORD LIKE THAT IN PRODUCTION. 
</code></pre>
</li>
</ol>
<p class="has-line-data" data-line-start="57" data-line-end="58">THE ONLY WAY TO STORE PASSWORD TO ENCRYPT/DECRYPT IS STORE PASSWORD AS ENVIRONMENT VARIABLE, IT SHOULD NEVER BE HARDCODED OR COMMITED TO ANY REPOSITORY, AND IT SHOULDN’T BE DISTURBED TO STAFF WITHOUT SECURITY RIGHTS. THIS METHOD IS POSSIBLE IN CODE ONLY FOR DEMONSTRATIVE PURPOSES]</p>
<p class="has-line-data" data-line-start="60" data-line-end="63">DECRYPT DATA<br>
[For that operation you need write script for table in PostgreSQL]<br>
This script:</p>
<p class="has-line-data" data-line-start="64" data-line-end="73">SELECT<br>
PGP_SYM_DECRYPT(name::bytea, ‘key’) as name,<br>
PGP_SYM_DECRYPT(email::bytea, ‘key’) as email,<br>
PGP_SYM_DECRYPT(gender::bytea, ‘key’) as gender,<br>
PGP_SYM_DECRYPT(degre::bytea, ‘key’) as degre,<br>
PGP_SYM_DECRYPT(university::bytea, ‘key’) as university<br>
From parser<br>
^<br>
^—&lt; You need to put your Values that you set in [First setup]</p>
<p class="has-line-data" data-line-start="80" data-line-end="84">[When it’s set]<br>
You can check if programm is working with file ‘Sheet1.html’.<br>
Drag ‘Sheet1.html’ to your desktop and then copy path to ‘Sheet1.html’<br>
and paste it as URL when program will ask you for URL</p>

