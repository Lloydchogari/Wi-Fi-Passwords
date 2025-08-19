import subprocess
import re
import locale

def get_wifi_passwords():
    encoding = locale.getpreferredencoding()

    # Get all Wi-Fi profiles
    profiles_data = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles'],
        shell=True
    ).decode(encoding, errors='ignore')

    profiles = re.findall(r"All User Profile\s*:\s(.*)", profiles_data)

    wifi_list = []
    for profile in profiles:
        profile = profile.strip()
        try:
            profile_info = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
                shell=True
            ).decode(encoding, errors='ignore')

            password_match = re.search(r"Key Content\s*:\s(.*)", profile_info)
            password = password_match.group(1) if password_match else "None"

            wifi_list.append((profile, password))

        except subprocess.CalledProcessError:
            # Skip profiles that cause errors
            wifi_list.append((profile, "Error retrieving password"))

    return wifi_list

if __name__ == "__main__":
    wifi_passwords = get_wifi_passwords()
    print("Saved Wi-Fi Passwords:\n")
    for ssid, password in wifi_passwords:
        print(f"SSID: {ssid}, Password: {password}")
