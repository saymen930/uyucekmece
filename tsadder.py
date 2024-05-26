from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import csv
import os
import pickle
import time

def load_accounts(file_path):
    accounts = []
    with open(file_path, 'rb') as f:
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
    return accounts

def authorize_accounts(accounts):
    authorized_accounts = []
    for account in accounts:
        client = TelegramClient(session_name, account[0], account[1])
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(account[2])
                code = input(f"Enter the code for {account[2]}: ")
                client.sign_in(account[2], code)
            except PhoneNumberBannedError:
                print(f"{account[2]} is banned.")
                continue
        authorized_accounts.append(account)
    return authorized_accounts

def join_group(accounts, group_link):
    for account in accounts:
        client = TelegramClient(session_name, account[0], account[1])
        client.connect()
        try:
            client(JoinChannelRequest(group_link))
            print(f"Joined group with {account[2]}")
        except Exception as e:
            print(f"Failed to join group with {account[2]}: {e}")
        client.disconnect()

def main():
    input_file = 'members/members.csv'
    session_name = 'sessions/session'
    group_link = input("Enter the group link: ")

    accounts = load_accounts('vars.txt')
    authorized_accounts = authorize_accounts(accounts)

    join_group(authorized_accounts, group_link)

    # Add further processing if needed

if __name__ == "__main__":
    main()
    
