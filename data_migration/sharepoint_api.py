"""
CONNECTS TO SHAREPOINT AND LISTS ALL SHAREPOINT FOLDERS AND FILES
"""
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

#Sharepoint class
class Sharepoint:
    ''' Sharepoint class with functions to connect and list folders and files '''
    # Function definition for getting Sharepoint connection
    def get_sharepoint_context_using_app(url,clientid,clientsecret):
        """Connect to the SharePoint ans return the Web name and URL of the SharePoint 
            :param url: URL of the SharePoint site from which data will be retrieved
            :param clientid: Client ID credential of the SharePoint Site
            :param clientsecret: Client Secret credential of the SharePoint Site
            :return: Web title
        """
        # Get sharepoint credentials
        sharepoint_url = url
        # Initialize the client credentials
        client_credentials = ClientCredential(clientid,clientsecret)
        # create client context object
        ctx = ClientContext(sharepoint_url).with_credentials(client_credentials)
        return ctx
# Function definition for getting FOLDER DETAILS
    def sharepoint_folder_details(ctx, folder_in_sharepoint):
        """Get the list of folders in the SharePoint 
            :param ctx: client context object
            :param folder_in_sharepoint: Path to the Sharepoint folder
            :return: Folder list 
        """
        try:
            folder = ctx.web.get_folder_by_server_relative_url(folder_in_sharepoint)
            folder_names = []
            sub_folders = folder.folders
            ctx.load(sub_folders)
            ctx.execute_query()
            for s_folder in sub_folders:
                folder_names.append(s_folder.properties["Name"])
            return folder_names
        except Exception as excep_type:
            print('Problem printing out library folder contents: ', excep_type)
            return None
# Function definition for FILE DETAILS
    def file_details(ctx, sub_folder_sharepoint):
        """Get the list of Files in the SharePoint SubFolder
            :param ctx: client context object
            :param sub_folder_sharepoint: Path to the Sharepoint Subfolder
            :return: Folder list 
        """
        try:
            sub_folder = ctx.web.get_folder_by_server_relative_url(sub_folder_sharepoint)
            file_names = []
            sub_folder_files = sub_folder.files
            ctx.load(sub_folder_files)
            ctx.execute_query()
            for s_folder in sub_folder_files:
                file_names.append(s_folder.properties["Name"])
            return file_names
        except Exception as excep_type:
            print('Problem printing out library file contents: ', excep_type)
            return None
    