import dropbox
import schedule
import time

#Reference to time
current_seconds = 0

#How often we are uploading
seconds = 30

#INSERT. Where we are sending to. In this case, dropbox
file_path = '/mri/'

#INSERT. Please insert your DropBox OAuth 2: Generated access token  Example: XbrL3eC3WIMA-qhvMsBHmBZMIpKMY3WbwZFJfR1sNsRNC
api_token = 'XbrL3eC3WIAAAAAAAAAE4vaEMA-qhvMsBHmBZMIpKMY3WbwZFJfrhyS1R1sNsRNC'

#dbx is dropbox object followed by the generated token
dbx_token = dropbox.Dropbox(api_token)

#INSERT. Enter the path of putty log file that you'll be uploading. Example: /home/pi/Desktop/mri.txt
putty_log = '/home/pi/Desktop/mri.txt'

#clearing log function
def clear_log():
    global current_seconds
    file = open(putty_log, 'w')
    #reducing file to 0 bits, essentially erasing its contents
    file.truncate(0)
    
    file.close()


#upload file function
def dropboxUpload():
    global current_seconds
    #file path that we are sending
    file = open(putty_log, 'rb')

    #uploads to dropbox (file_directory,dropbox_directory/file_name)
    dbx_token.files_upload(file.read(), file_path + str(current_seconds) + ".txt")
    #/mri/30.txt
    #Example: dbx_token.files_upload(putty_log, 'rb'.read(), "/mri/" + "putty" + "/.txt"
    file.close()
    
    clear_log()




#schedules every 30 seconds for function to run
schedule.every(seconds).seconds.do(dropboxUpload)

def dropBox():
    global current_seconds
    
    dropboxUpload()
    
    while current_seconds < 86400:
        #Proceeding line keeps the schedule.every() functions continuously occuring
        schedule.run_pending()
        #forcibly making Python wait one second
        time.sleep(1)
        current_seconds += 1
        #delete drop_box folder
    dbx_token.files_delete(file_path)




def main():
    while True:
        clear_log()
        dropBox()
        clear_log()
    

main()