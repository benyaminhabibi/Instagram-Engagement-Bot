from colorama import Fore , init , Style
from modules import banner
import os, platform
from modules.instagram_bot import InstagramBot
import argparse
from modules.profile_scraper import get_profile_info
from modules.post_scraper import get_posts_data
from modules.engagement_calculator import calculate_engagement_rate

# It gives us the ability to show colors in CMD
init(autoreset=True)

def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def main():
    clear_terminal()
    banner.banner()
    # CLI Settings
    parser = argparse.ArgumentParser(description="Instagram bot to calculate the rate of interaction")
    parser.add_argument('--username', required=True, type=str, help="Instagram username for login")
    parser.add_argument('--password', required=True, type=str, help="Instagram password for login")
    parser.add_argument('--target', required=True, type=str, help="ID Instagram page for analysis")
    parser.add_argument('--graphic', default='enable', required=False, type=str, help="Graphic mode (enable/disable)")
    parser.add_argument('--num', default=5, required=False, type=int, help="Number of posts to extract (only digits)")
    args = parser.parse_args()

    if args.graphic == 'enable':
        bot = InstagramBot(graphic_mode=True)
    elif args.graphic == 'disable':
        bot = InstagramBot(graphic_mode=False)
    else:
        print(Fore.RED + 'ّ\nInvalid graphic mode (enable or disable)' + Style.RESET_ALL)
        return

    try:
        if not bot.login(args.username, args.password):
            print(Fore.RED + "\nLogin failed, Check the Username and Password." + Style.RESET_ALL)
            return

        profile_info = get_profile_info(bot.get_driver(), args.target)
        if not profile_info:
            print(Fore.RED + "\nCannot extract profile information." + Style.RESET_ALL)
            return

        posts = get_posts_data(bot.get_driver(), args.target, num_posts=args.num)
        if not posts:
            print(Fore.RED + "\nCannot extract posts information." + Style.RESET_ALL)
            return

        engagement_rate, avg_likes, avg_comments = calculate_engagement_rate(posts, profile_info["followers"])

        output = f"""\n
        Instagram page analysis: {args.target}
        Followers: {profile_info['followers']}
        Followings: {profile_info['following']}
        Average likes for last {args.num}: {avg_likes:.1f}
        Average comments for last {args.num}: {avg_comments:.1f}
        Engagement rate: {engagement_rate}%
        """
        print(output)
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write(output)
    finally:
        bot.quit()

if __name__ == "__main__":
    main()