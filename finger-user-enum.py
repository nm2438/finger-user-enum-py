#!/usr/bin/python3

import subprocess
import argparse
import threading 


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='userfile', help='wordlist to use for potential usernames')
    parser.add_argument(dest='rhost', help='ip address of target host')
    parser.add_argument('-q', dest='quiet', action='store_true', required=False, help='suppress running output')
    parser.add_argument('-t', dest='threadcount', required=False, default=1, type=int)
    parser.add_argument('-o', dest='out', required=False, help='path to output file')
    return parser.parse_args()


def test_users(userlist, found_users, rhost, quietmode):
    for user in userlist:
        try:
            out = subprocess.check_output(f'finger {user}@{rhost} 2>/dev/null', shell=True).decode('utf-8')
            outputlines = split_out[1:] if len(split_out:=out.split('\n')) > 1 else [out]
            for line in outputlines:
                if len(splitline:=line.strip().split()) > 2 and splitline!=['Login','Name','TTY','Idle','When','Where']:
                    new_user = splitline[0]
                    if not quietmode:
                        print(f"{'-'*80}\nFound: {new_user}\n{line}\n{'-'*80}")
                    found_users.append(new_user)
        except Exception as e:
            print(f"Error while checking {user}:\n\t{e}")


def main():
    args = parse_args()
    with open(args.userfile, 'r') as f:
        users_to_test = [line.strip() for line in f.readlines()]
    found_users = []
    threads = []
    thread_size = \
        ( len(users_to_test) // args.threadcount ) + \
        (1 if len(users_to_test) % args.threadcount != 0 else 0)
    for i in range(args.threadcount):
        start = i * thread_size
        end = min(start+thread_size, len(users_to_test))
        test_subset = users_to_test[start:end]
        thrd = threading.Thread(target=test_users, args=(test_subset, found_users, args.rhost, args.quiet,))
        threads.append(thrd)
        thrd.start()
    for thread in threads:
        thread.join()
    found_users = list(set(found_users))
    if args.out:
        with open(args.out, 'w') as f:
            for user in found_users:
                f.write(user + '\n')
    else:
        print(f"\n{'-'*40}\nScript Finished. Found {len(found_users)} usernames.\n{'-'*40}")
        for user in found_users:
            print(user)


if __name__=="__main__":
    main()