from datetime import datetime
import json
import time
from colorama import Fore
import requests
import random

class otterloot:
    BASE_URL = "https://otter-game-service.otterloot.io/api/"
    HEADERS = {
        "accept": "*/*:",
        "accept-encoding": "gzip, deflate, br, zstd:",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8:",
        "content-type": "application/json",
        "origin": "https://assets.otterloot.io",
        "priority": "u=1, i",
        "referer": "https://assets.otterloot.io/",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131":',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0" 
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.energy = 0

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Otter Loot Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
            print(Fore.LIGHTBLACK_EX + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |") + " " + color + message + Fore.RESET)

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log("❌ Failed to parse config.json. Please check the file format.", Fore.RED)
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("🔐 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("🚫 Invalid login index. Please check again.", Fore.RED)
            return

        req_url = f"{self.BASE_URL}v1/auth/login"
        token = self.query_list[index]

        self.log(
            f"🔑 Using token: {token[:10]}... (truncated for security)",
            Fore.CYAN,
        )

        payload = {"initData": token}

        try:
            self.log(
                "📤 Sending request to log in...",
                Fore.CYAN,
            )

            response = requests.post(req_url, headers=self.HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                access_token = data.get("data", {}).get("accessToken")
                if access_token:
                    self.token = access_token
                    self.log("✅ Access token successfully retrieved.", Fore.GREEN)
                    self.log(f"🔓 Access Token: {access_token[:10]}... (truncated for security)", Fore.LIGHTGREEN_EX)
                else:
                    self.log("⚠️ Access token not found in response.", Fore.YELLOW)
            else:
                error_code = data.get("code", "Unknown")
                self.log(f"❌ Login failed with error code: {error_code}", Fore.RED)

        except requests.exceptions.RequestException as e:
            self.log(f"🚨 Failed to send login request: {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"⚠️ Data error (possible JSON issue): {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
        except KeyError as e:
            self.log(f"🚫 Key error: {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❗ Unexpected error: {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)

    def info(self) -> dict:
        """Fetches and logs user profile information from the server."""
        req_url_profile = f"{self.BASE_URL}v1/user/profile"
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

        try:
            self.log("📡 Fetching user profile information...", Fore.CYAN)
            response = requests.get(req_url_profile, headers=headers)
            response.raise_for_status()

            profile_data = response.json()
            if not profile_data.get("success", False):
                raise ValueError("Failed to fetch profile data. Check the API response.")

            user_data = profile_data.get("data", {})
            if not user_data:
                raise ValueError("User data is missing in the response.")

            user_id = user_data.get("id", "Unknown")
            first_name = user_data.get("firstName", "Unknown")
            last_name = user_data.get("lastName", "Unknown")
            language = user_data.get("language", "Unknown")
            avatar_id = user_data.get("avatarId", "Unknown")

            self.log(f"✅ User profile retrieved successfully:", Fore.GREEN)
            self.log(f"👤 ID: {user_id}", Fore.LIGHTGREEN_EX)
            self.log(f"📛 Name: {first_name} {last_name}".strip(), Fore.LIGHTGREEN_EX)
            self.log(f"🌐 Language: {language}", Fore.LIGHTGREEN_EX)
            self.log(f"🖼️ Avatar ID: {avatar_id}", Fore.LIGHTGREEN_EX)

            return user_data

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch profile: {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            return {}
        except ValueError as e:
            self.log(f"❌ Data error: {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            return {}
        except Exception as e:
            self.log(f"❗ An unexpected error occurred: {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            return {}

    def info_game(self) -> dict:
        """Fetches and logs game info from the server."""
        req_url_game_info = f"{self.BASE_URL}v1/game/info"
        headers = {
            **self.HEADERS,
            "authorization": f"Bearer {self.token}"
        }

        try:
            self.log("📡 Fetching game info...", Fore.CYAN)
            response = requests.get(req_url_game_info, headers=headers)
            response.raise_for_status()

            game_data = response.json()
            if not game_data.get("success", False):
                raise ValueError("Failed to fetch game info. Check the API response.")

            data = game_data.get("data", {})
            if not data:
                raise ValueError("Game data is missing in the response.")

            # Extract relevant data
            self.energy = data.get("energy", 0)
            max_energy = data.get("maxEnergy", 0)
            last_regen = data.get("lastRegenEnergy", "Unknown")
            next_regen = data.get("nextRegenEnergy", "Unknown")
            target_user = data.get("target", {}).get("user", {})
            target_otter = data.get("target", {}).get("otter", {})
            coin_can_steal = data.get("target", {}).get("coinCanSteal", {}).get("amount", {}).get("value", 0)

            # Log game information
            self.log(f"⚡ Energy: {self.energy}/{max_energy}", Fore.LIGHTGREEN_EX)
            self.log(f"⏳ Last Regen: {last_regen}", Fore.LIGHTGREEN_EX)
            self.log(f"⏳ Next Regen: {next_regen}", Fore.LIGHTGREEN_EX)

            if target_user:
                self.log(f"🎯 Target User ID: {target_user.get('id', 'Unknown')}", Fore.LIGHTGREEN_EX)
                self.log(f"📛 Name: {target_user.get('firstName', 'Unknown')} {target_user.get('lastName', '').strip()}", Fore.LIGHTGREEN_EX)
                self.log(f"🖼️ Avatar ID: {target_user.get('avatarId', 'Unknown')}", Fore.LIGHTGREEN_EX)

            if target_otter:
                self.log(f"🦦 Otter ID: {target_otter.get('id', 'Unknown')}", Fore.LIGHTGREEN_EX)
                self.log(f"⭐ Otter Level: {target_otter.get('level', 0)}", Fore.LIGHTGREEN_EX)
                self.log(f"💫 Total Stars: {target_otter.get('totalStars', 0)}", Fore.LIGHTGREEN_EX)

            self.log(f"💰 Coins Stealable: {coin_can_steal}", Fore.LIGHTGREEN_EX)

            return data

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch game info: {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            return {}
        except ValueError as e:
            self.log(f"❌ Data error: {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            return {}
        except Exception as e:
            self.log(f"❗ An unexpected error occurred: {e}", Fore.RED)
            if response is not None:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            return {}

    def spin(self) -> None:
        """Performs a spin in the game and handles rewards, stealing logic, or raids."""
        self.info_game()  
        while self.energy > 0:
            req_url_spin = f"{self.BASE_URL}v1/game/spin"
            headers = {
                **self.HEADERS,
                "authorization": f"Bearer {self.token}"
            }
            payload = {"x": 1}

            try:
                # Perform the spin
                self.log("🎰 Performing a spin...", Fore.CYAN)
                response = requests.post(req_url_spin, headers=headers, json=payload)
                response.raise_for_status()

                spin_data = response.json()
                if not spin_data.get("success", False):
                    raise ValueError("Spin request failed. Check the API response.")

                data = spin_data.get("data", {})
                if not data:
                    raise ValueError("Spin data is missing in the response.")

                slots = [slot.get("item") for slot in data.get("slots", [])]
                sum_rewards = data.get("sumRewards", [])

                # Log spin result
                self.log(f"🎲 Slots: {' | '.join(map(str, slots))}", Fore.LIGHTGREEN_EX)

                # Deduct energy after each spin
                self.energy -= 1
                self.log(f"⚡ Energy remaining: {self.energy}", Fore.MAGENTA)

                # Check if all slots are 5
                if all(slot == 5 for slot in slots):
                    self.log("💥 Jackpot! All slots are 5! Initiating steal attempts...", Fore.YELLOW)
                    self.perform_steal_attempts()

                # Check if all slots are 4
                elif all(slot == 4 for slot in slots):
                    self.log("🛡️ Raid opportunity! All slots are 4! Fetching raid information...", Fore.YELLOW)
                    self.perform_raid()

                else:
                    # Handle rewards
                    if sum_rewards:
                        for reward in sum_rewards:
                            kind = reward.get("kind", "Unknown")
                            reward_type = reward.get("type", "Unknown")
                            amount = reward.get("amount", {}).get("value", 0)
                            self.log(f"💎 Reward: Kind {kind}, Type {reward_type}, Amount: {amount}", Fore.LIGHTGREEN_EX)
                    else:
                        self.log("🎁 No rewards from this spin.", Fore.YELLOW)

            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to perform spin: {e}", Fore.RED)
                if response is not None:
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
            except ValueError as e:
                self.log(f"❌ Data error: {e}", Fore.RED)
                if response is not None:
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
            except Exception as e:
                self.log(f"❗ An unexpected error occurred: {e}", Fore.RED)
                if response is not None:
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
                    
            if self.energy == 0:
                self.log("🔄 Energy depleted. Updating game information...", Fore.BLUE)
                self.info_game()  

    def perform_raid(self) -> None:
        """Handles raid logic when all slots are 4."""
        raid_info_url = f"{self.BASE_URL}v1/game/raid-info"
        raid_url = f"{self.BASE_URL}v1/game/raid"
        headers = {
            **self.HEADERS,
            "authorization": f"Bearer {self.token}"
        }

        try:
            # Fetch raid information
            self.log("🔍 Fetching raid information...", Fore.CYAN)
            raid_info_response = requests.get(raid_info_url, headers=headers)
            raid_info_response.raise_for_status()

            raid_info_data = raid_info_response.json()
            if not raid_info_data.get("success", False):
                raise ValueError("Raid info request failed. Check the API response.")

            target_user = raid_info_data["data"]["user"]
            target_otter = raid_info_data["data"]["otter"]

            self.log(f"🎯 Target User: {target_user['firstName']}", Fore.LIGHTGREEN_EX)
            self.log(f"🦦 Target Otter Level: {target_otter['level']}, Stars: {target_otter['totalStars']}", Fore.LIGHTGREEN_EX)

            # Find the target part to raid
            parts = target_otter["parts"]
            broken_parts = [part for part in parts if part["broken"]]

            if broken_parts:
                # Prioritize broken parts with the lowest stars
                target_part = min(broken_parts, key=lambda x: x["stars"])
            else:
                # If no broken parts, choose the part with the lowest stars
                target_part = min(parts, key=lambda x: x["stars"])

            self.log(f"⚔️ Targeting part type: {target_part['type']} (Stars: {target_part['stars']}, Broken: {target_part['broken']})", Fore.YELLOW)

            # Perform raid
            raid_payload = {
                "goldenPunch": False,
                "part": target_part["type"],
                "type": 1,
                "userId": target_user["id"]
            }

            self.log("⚔️ Initiating raid...", Fore.YELLOW)
            raid_response = requests.post(raid_url, headers=headers, json=raid_payload)
            raid_response.raise_for_status()

            raid_data = raid_response.json()
            if not raid_data.get("success", False):
                self.log("❌ Raid failed. No rewards obtained.", Fore.RED)

                # Check if golden punch is available
                golden_punch_info = raid_data["data"].get("goldenPunch", {})
                if golden_punch_info.get("canPunch", False):
                    self.log("✨ Golden Punch is available! Fetching raid info again for efficiency...", Fore.CYAN)

                    # Fetch raid information again
                    raid_info_response = requests.get(raid_info_url, headers=headers)
                    raid_info_response.raise_for_status()
                    raid_info_data = raid_info_response.json()

                    if not raid_info_data.get("success", False):
                        raise ValueError("Raid info request failed after golden punch.")

                    target_user = raid_info_data["data"]["user"]
                    target_otter = raid_info_data["data"]["otter"]

                    # Re-select the target part
                    parts = target_otter["parts"]
                    broken_parts = [part for part in parts if part["broken"]]

                    if broken_parts:
                        target_part = min(broken_parts, key=lambda x: x["stars"])
                    else:
                        target_part = min(parts, key=lambda x: x["stars"])

                    self.log(f"⚔️ Retargeting part type: {target_part['type']} (Stars: {target_part['stars']}, Broken: {target_part['broken']})", Fore.YELLOW)

                    # Perform golden punch raid
                    raid_payload["goldenPunch"] = True
                    self.log("✨ Initiating Golden Punch raid...", Fore.YELLOW)
                    raid_response = requests.post(raid_url, headers=headers, json=raid_payload)
                    raid_response.raise_for_status()

                    raid_data = raid_response.json()

                    if raid_data.get("success", False):
                        reward = raid_data["data"]["reward"]
                        self.log(f"🏆 Golden Punch Reward: Kind {reward['kind']}, Type {reward['type']}, Amount: {reward['amount']['value']}", Fore.LIGHTGREEN_EX)
                    else:
                        self.log("❌ Golden Punch raid failed.", Fore.RED)

                return

            reward = raid_data["data"]["reward"]
            self.log(f"🏆 Raid Reward: Kind {reward['kind']}, Type {reward['type']}, Amount: {reward['amount']['value']}", Fore.LIGHTGREEN_EX)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch raid information or perform raid: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error during raid: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❗ An unexpected error occurred during raid: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)

    def perform_steal_attempts(self) -> None:
        """Performs steal attempts until an error or success condition is met."""
        req_url_steal = f"{self.BASE_URL}v1/game/steal"
        headers = {
            **self.HEADERS,
            "authorization": f"Bearer {self.token}"
        }

        max_errors = 5  # Stop after 5 consecutive errors
        error_count = 0
        used_positions = set()

        while error_count < max_errors:
            position = random.randint(1, 5)

            # Skip already used positions
            if position in used_positions:
                continue

            payload = {"position": position}
            used_positions.add(position)

            try:
                self.log(f"🚀 Attempting to steal at position {position}...", Fore.CYAN)
                response = requests.post(req_url_steal, headers=headers, json=payload)
                response.raise_for_status()

                steal_data = response.json()

                if not steal_data.get("success", False):
                    self.log(f"⚠️ Steal attempt failed: {steal_data.get('message', 'Unknown error')}", Fore.YELLOW)
                    
                    # Check if the error is related to the target or limit
                    if "target" in steal_data.get("message", "").lower():
                        continue  # Skip and try again
                    elif "limit" in steal_data.get("message", "").lower():
                        self.log("⛔ Limit reached, stopping attempts.", Fore.RED)
                        break

                    error_count += 1
                    continue

                reward = steal_data.get("data", {}).get("reward", {})
                if reward:
                    kind = reward.get("kind", "Unknown")
                    reward_type = reward.get("type", "Unknown")
                    amount = reward.get("amount", {}).get("value", 0)
                    self.log(f"💰 Steal Success: Kind {kind}, Type {reward_type}, Amount: {amount}", Fore.LIGHTGREEN_EX)
                    break  # Stop if steal was successful
                else:
                    self.log(f"🎯 Attempt failed: No reward found.", Fore.YELLOW)
                    error_count += 1

            except requests.exceptions.RequestException as e:
                self.log(f"❌ Request failed: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                error_count += 1
            except Exception as e:
                self.log(f"❗ An unexpected error occurred: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                error_count += 1

        if error_count >= max_errors:
            self.log("🛑 Maximum error limit reached. Stopping attempts.", Fore.RED)

    def quest(self) -> None:
        """Fetches available quests and special quests, then attempts to complete them."""
        
        def fetch_and_complete_quests(req_url: str, quest_type: str) -> None:
            headers = {
                **self.HEADERS,
                "authorization": f"Bearer {self.token}"
            }

            try:
                self.log(f"📋 Fetching {quest_type} quests...", Fore.CYAN)
                response = requests.get(req_url, headers=headers)
                response.raise_for_status()

                quest_data = response.json()
                if not quest_data.get("success", False):
                    self.log(f"⚠️ Failed to fetch {quest_type} quest list.", Fore.YELLOW)
                    return

                quests = quest_data.get("data", {}).get("quests", [])
                if not quests:
                    self.log(f"⚠️ No available {quest_type} quests.", Fore.YELLOW)
                    return

                for quest in quests:
                    quest_id = quest.get("questID")
                    quest_status = quest.get("questStatus")

                    # Skip if quest is already completed
                    if quest_status != 1:
                        continue

                    payload = {"questID": quest_id}
                    req_url_quest = f"{self.BASE_URL}v1/quest/do"

                    try:
                        self.log(f"🗺️ Attempting {quest_type} quest ID: {quest_id} - {quest.get('description', 'No description')}...", Fore.CYAN)
                        response = requests.post(req_url_quest, headers=headers, json=payload)
                        response.raise_for_status()

                        quest_done_data = response.json()
                        if not quest_done_data.get("success", False):
                            self.log(f"⚠️ {quest_type} quest ID {quest_id} failed or is not available.", Fore.YELLOW)
                            continue

                        data = quest_done_data.get("data", {})
                        if not data:
                            self.log(f"⚠️ No data received for {quest_type} quest ID {quest_id}.", Fore.YELLOW)
                            continue

                        # Log quest completion
                        quest_done_id = data.get("questDoneID", "Unknown")
                        self.log(f"✅ {quest_type.capitalize()} quest {quest_done_id} completed successfully!", Fore.LIGHTGREEN_EX)

                        # Handle rewards
                        rewards = data.get("rewards", [])
                        if rewards:
                            for reward in rewards:
                                kind = reward.get("kind", "Unknown")
                                reward_type = reward.get("type", "Unknown")
                                amount = reward.get("amount", {}).get("value", 0)
                                self.log(f"🎁 Reward: Kind {kind}, Type {reward_type}, Amount: {amount}", Fore.LIGHTGREEN_EX)
                        else:
                            self.log(f"🎁 No rewards for {quest_type} quest ID {quest_done_id}.", Fore.YELLOW)

                        # Check if there's a next quest
                        next_quest = data.get("nextQuest")
                        if next_quest is None:
                            self.log(f"🏁 No more {quest_type} quests available.", Fore.CYAN)
                            break

                    except requests.exceptions.RequestException as e:
                        self.log(f"❌ Failed to perform {quest_type} quest ID {quest_id}: {e}", Fore.RED)
                        self.log(f"📄 Response content: {response.text}", Fore.RED)
                    except ValueError as e:
                        self.log(f"❌ Data error for {quest_type} quest ID {quest_id}: {e}", Fore.RED)
                        self.log(f"📄 Response content: {response.text}", Fore.RED)
                    except Exception as e:
                        self.log(f"❗ An unexpected error occurred for {quest_type} quest ID {quest_id}: {e}", Fore.RED)
                        self.log(f"📄 Response content: {response.text}", Fore.RED)

            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to fetch {quest_type} quest list: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            except ValueError as e:
                self.log(f"❌ Data error while fetching {quest_type} quest list: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            except Exception as e:
                self.log(f"❗ An unexpected error occurred while fetching {quest_type} quest list: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)

        # Process regular quests
        fetch_and_complete_quests(f"{self.BASE_URL}v1/quest", "regular")

        # Process special quests
        fetch_and_complete_quests(f"{self.BASE_URL}v1/special-quest", "special")

    def otter(self) -> None:
        """Fetches Otter details, repairs broken parts, and upgrades parts until max or limit reached."""
        req_url_otter = f"{self.BASE_URL}v1/otter"
        headers = {
            **self.HEADERS,
            "authorization": f"Bearer {self.token}"
        }

        try:
            # Fetch Otter details
            self.log("🐾 Fetching Otter details...", Fore.CYAN)
            response = requests.get(req_url_otter, headers=headers)
            response.raise_for_status()

            otter_data = response.json()
            if not otter_data.get("success", False):
                self.log("⚠️ Failed to fetch Otter details.", Fore.YELLOW)
                return

            data = otter_data.get("data", {})
            if not data:
                self.log("⚠️ No data received for Otter details.", Fore.YELLOW)
                return

            parts = data.get("parts", [])
            total_stars = data.get("totalStars", 0)
            self.log(f"🦦 Otter Level: {data.get('level', 0)} | Total Stars: {total_stars}", Fore.LIGHTGREEN_EX)

            total_medals = 0  # Track total medals earned

            # Repair broken parts
            for part in parts:
                try:
                    if part.get("broken", False):
                        part_type = part.get("type")
                        self.log(f"🔧 Repairing broken part type {part_type}...", Fore.YELLOW)
                        repair_url = f"{self.BASE_URL}v1/otter/repair"
                        repair_payload = {"part": part_type}
                        repair_response = requests.post(repair_url, headers=headers, json=repair_payload)
                        repair_response.raise_for_status()
                        repair_data = repair_response.json()
                        if repair_data.get("success", False):
                            self.log("✅ Repair successful!", Fore.LIGHTGREEN_EX)
                        else:
                            self.log(f"❌ Repair failed for part type {part_type}.", Fore.RED)
                            self.log(f"📄 Response content: {response.text}", Fore.RED)
                except Exception as e:
                    self.log(f"❌ Error repairing part type {part.get('type')}: {e}", Fore.RED)
                    self.log(f"📄 Response content: {response.text}", Fore.RED)

            # Upgrade parts
            for part in parts:
                try:
                    while total_medals < 200:  # Loop until we reach the medal limit
                        if part.get("stars", 0) < 3 and not part.get("broken", False):
                            part_type = part.get("type")
                            self.log(f"⬆️ Upgrading part type {part_type}...", Fore.CYAN)
                            upgrade_url = f"{self.BASE_URL}v1/otter/upgrade"
                            upgrade_payload = {"part": part_type}
                            upgrade_response = requests.post(upgrade_url, headers=headers, json=upgrade_payload)
                            upgrade_response.raise_for_status()
                            upgrade_data = upgrade_response.json()

                            if upgrade_data.get("success", False):
                                # Check if the error is due to insufficient coins
                                if "not enough coins" in upgrade_data.get("message", "").lower():
                                    self.log(f"💰 Not enough coins to upgrade part type {part_type}.", Fore.RED)
                                else:
                                    self.log(f"❌ Upgrade failed for part type {part_type}.", Fore.RED)
                            else:
                                medal = upgrade_data.get("data", {}).get("medal", 0)
                                total_medals += medal
                                self.log(f"🏅 Upgrade successful! Earned {medal} medals. Total medals: {total_medals}", Fore.LIGHTGREEN_EX)

                                if total_medals >= 200:
                                    self.log("🏁 Total medals reached 200. Stopping upgrades.", Fore.LIGHTMAGENTA_EX)
                                    break
                        else:
                            break
                except Exception as e:
                    self.log(f"❌ Error upgrading part type {part.get('type')}: {e}", Fore.RED)

            self.log("✅ Finished processing all parts.", Fore.LIGHTMAGENTA_EX)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to perform Otter operations: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error during Otter operations: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❗ An unexpected error occurred during Otter operations: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)

    def buy(self, type: str = "gold") -> None:
        """Handles purchase operations in the Otter game.

        Args:
            type (str): The type of item to buy. Defaults to 'gold'.
        """
        shop_url = f"{self.BASE_URL}shop/buy-currency"
        headers = {
            **self.HEADERS,
            "authorization": f"Bearer {self.token}"
        }

        # Determine payload based on type
        if type == "gold":
            payload = {"packID": 3, "packType": 2}
        elif type == "energy":
            payload = {"packID": 3, "packType": 3}
        else:
            self.log(f"❌ Invalid purchase type: {type}", Fore.RED)
            return

        try:
            self.log(f"🛒 Attempting to buy {type}...", Fore.CYAN)
            response = requests.post(shop_url, headers=headers, json=payload)
            response.raise_for_status()

            response_data = response.json()
            if not response_data.get("success", False):
                self.log(f"❌ Purchase failed. Message: {response_data.get('message', 'No message provided.')}", Fore.RED)
                return

            self.log(f"✅ Successfully purchased {type}.", Fore.LIGHTGREEN_EX)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to perform Otter operations: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error during Otter operations: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❗ An unexpected error occurred during Otter operations: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)

if __name__ == "__main__":
    otter = otterloot()
    index = 0
    max_index = len(otter.query_list)
    config = otter.load_config()

    otter.log("🎉 [LIVEXORDS] === Welcome to Otter Loot Automation === [LIVEXORDS]", Fore.YELLOW)
    otter.log(f"📂 Loaded {max_index} accounts from query list.", Fore.LIGHTBLUE_EX)

    while True:
        current_account = otter.query_list[index]
        display_account = current_account[:10] + "..." if len(current_account) > 10 else current_account

        otter.log(f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}", Fore.LIGHTGREEN_EX)

        otter.login(index)
        otter.info()

        otter.log("🛠️ Starting task execution...", Fore.CYAN)
        tasks = {
            "spin": "🎰 Spin the Wheel",
            "quest": "📜 Quest Solver",
            "otter": "🦦 Otter Manager",
            "buy": "💰 Purchase Items",
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            otter.log(f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}", Fore.YELLOW if task_status else Fore.RED)

            if task_status:
                otter.log(f"🔄 Executing {task_name}...", Fore.CYAN)
                if task_key == "buy":
                    type_buy = config.get("type_buy", "gold")
                    otter.buy(type_buy)
                else:
                    getattr(otter, task_key)()

        if index == max_index - 1:
            otter.log("🔁 All accounts processed. Restarting loop.", Fore.LIGHTGREEN_EX)
            otter.log(f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting.", Fore.CYAN)
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            otter.log(f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds.", Fore.CYAN)
            time.sleep(config.get("delay_account_switch", 10))
            index += 1
