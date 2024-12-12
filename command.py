from turtle import st
import paramiko
import os


def excute_remote_command(config,progress_callback,cmd):
    # SSH connection details
    hostname = config.get('hostname')
    port = config.get('port')
    username = config.get('username')
    password = config.get('password')
    '''
    service  type list [
        {
            "label": "production server",
            "name": "deeper.service",
        },
        {
            "label": "qa server",
            "name": "deepertest.service",
        }
    ]

    '''

    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    total_tasks =  1  # Total number of tasks including dumping tables, procedures, and functions
    completed_tasks = 0  # Track completed tasks
    
    # Connect to the server
    try:
        client.connect(hostname, port, username, password)
        print("Connected to the server!")

        current_dir = '/root'  # Initial directory
        # Prepend cd command to change directory before executing the command
        command_to_execute = f'cd {current_dir} && {cmd}'
        
        # Execute the modified command on the remote server
        stdin, stdout, stderr = client.exec_command(command_to_execute)
        if progress_callback is not None:
            completed_tasks += 1
            progress_callback(completed_tasks, total_tasks)

        # Read the output of the command
        for line in stdout:
            print(line.strip())


        '''
        # Update current directory if cd command is detected in the user input
        if cmd.startswith("cd "):
            # Extract the new directory from the command
            new_dir = cmd.split(" ", 1)[1]
            if new_dir.startswith("/"):  # Check if it's an absolute path
                current_dir = new_dir
            else:  # Otherwise, treat it as a relative path
                current_dir = os.path.normpath(os.path.join(current_dir, new_dir))
        '''
    finally:
        # Close the SSH connection
        client.close()
