from datetime import datetime
import time
from colorama import Fore
import requests
import random
from fake_useragent import UserAgent
import asyncio
import json
import gzip
import brotli
import zlib
import chardet
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    }

    def __init__(self):
        self.config = self.load_config()
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.energy = 0
        self.session = self.sessions()
        self._original_requests = {
            "get": requests.get,
            "post": requests.post,
            "put": requests.put,
            "delete": requests.delete,
        }
        self.proxy_session = None

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Otter Loot Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode('utf-8', 'backslashreplace').decode('utf-8')
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )
    
    def sessions(self):
        session = requests.Session()
        retries = Retry(
            total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504, 520]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    def decode_response(self, response):
        """
        Mendekode response dari server secara umum.

        Parameter:
            response: objek requests.Response

        Mengembalikan:
            - Jika Content-Type mengandung 'application/json', maka mengembalikan objek Python (dict atau list) hasil parsing JSON.
            - Jika bukan JSON, maka mengembalikan string hasil decode.
        """
        # Ambil header
        content_encoding = response.headers.get("Content-Encoding", "").lower()
        content_type = response.headers.get("Content-Type", "").lower()

        # Tentukan charset dari Content-Type, default ke utf-8
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip()

        # Ambil data mentah
        data = response.content

        # Dekompresi jika perlu
        try:
            if content_encoding == "gzip":
                data = gzip.decompress(data)
            elif content_encoding in ["br", "brotli"]:
                data = brotli.decompress(data)
            elif content_encoding in ["deflate", "zlib"]:
                data = zlib.decompress(data)
        except Exception:
            # Jika dekompresi gagal, lanjutkan dengan data asli
            pass

        # Coba decode menggunakan charset yang didapat
        try:
            text = data.decode(charset)
        except Exception:
            # Fallback: deteksi encoding dengan chardet
            detection = chardet.detect(data)
            detected_encoding = detection.get("encoding", "utf-8")
            text = data.decode(detected_encoding, errors="replace")

        # Jika konten berupa JSON, kembalikan hasil parsing JSON
        if "application/json" in content_type:
            try:
                return json.loads(text)
            except Exception:
                # Jika parsing JSON gagal, kembalikan string hasil decode
                return text
        else:
            return text

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
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
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
                    self.log(
                        f"🔓 Access Token: {access_token[:10]}... (truncated for security)",
                        Fore.LIGHTGREEN_EX,
                    )
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
                raise ValueError(
                    "Failed to fetch profile data. Check the API response."
                )

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
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

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
            coin_can_steal = (
                data.get("target", {})
                .get("coinCanSteal", {})
                .get("amount", {})
                .get("value", 0)
            )

            # Log game information
            self.log(f"⚡ Energy: {self.energy}/{max_energy}", Fore.LIGHTGREEN_EX)
            self.log(f"⏳ Last Regen: {last_regen}", Fore.LIGHTGREEN_EX)
            self.log(f"⏳ Next Regen: {next_regen}", Fore.LIGHTGREEN_EX)

            if target_user:
                self.log(
                    f"🎯 Target User ID: {target_user.get('id', 'Unknown')}",
                    Fore.LIGHTGREEN_EX,
                )
                self.log(
                    f"📛 Name: {target_user.get('firstName', 'Unknown')} {target_user.get('lastName', '').strip()}",
                    Fore.LIGHTGREEN_EX,
                )
                self.log(
                    f"🖼️ Avatar ID: {target_user.get('avatarId', 'Unknown')}",
                    Fore.LIGHTGREEN_EX,
                )

            if target_otter:
                self.log(
                    f"🦦 Otter ID: {target_otter.get('id', 'Unknown')}",
                    Fore.LIGHTGREEN_EX,
                )
                self.log(
                    f"⭐ Otter Level: {target_otter.get('level', 0)}",
                    Fore.LIGHTGREEN_EX,
                )
                self.log(
                    f"💫 Total Stars: {target_otter.get('totalStars', 0)}",
                    Fore.LIGHTGREEN_EX,
                )

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
        """
        Melakukan spin dalam game dengan beberapa fase:
        
        🔰 **Phase 0: Persiapan**
        - Memperbarui info game dan memeriksa energy.
        
        🚀 **Phase 1: Mengirim Permintaan Spin**
        - Mengirim request ke API dengan payload yang mengirimkan
            hingga 3 spin sekaligus (disesuaikan dengan energy yang ada).
        
        🔍 **Phase 2: Memvalidasi dan Memproses Respons Spin**
        - Mengecek status, mengurangi energy sesuai jumlah spin,
            dan menampilkan hasil slot.
        
        🎯 **Phase 3: Menangani Hasil Spin**
        - Jika semua slot bernilai 5, akan dilakukan steal attempt.
            Jika semua slot bernilai 4, akan dilakukan raid.
            Jika tidak, maka reward lain akan di-handle.
        """
        # 🔰 Phase 0: Persiapan - Update informasi game terlebih dahulu
        self.info_game()

        while True:
            if self.energy <= 0:
                self.log("🔄 Energy depleted. Updating game information...", Fore.BLUE)
                self.info_game()
                break

            time.sleep(1)
            self.log("🎰 Initiating spin process...", Fore.CYAN)

            # Tentukan berapa kali spin yang dilakukan dalam satu request.
            spins_to_perform = min(3, self.energy)
            payload = {"x": spins_to_perform}

            # 🚀 Phase 1: Mengirim Permintaan Spin
            def perform_spin_request() -> dict:
                req_url_spin = f"{self.BASE_URL}v1/game/spin"
                headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
                self.log(f"🎰 Performing {spins_to_perform} spin(s)...", Fore.CYAN)
                try:
                    response = requests.post(req_url_spin, headers=headers, json=payload)
                    try:
                        spin_data = response.json()
                    except Exception as json_error:
                        self.log("❌ Gagal parsing respons spin sebagai JSON.", Fore.RED)
                        raise json_error

                    # Jika status code bukan 200, periksa pesan error
                    if response.status_code != 200:
                        message = spin_data.get("message", "")
                        if "Can't spin, get steal target first" in message:
                            self.log("Can't spin, get steal target first. Initiating steal attempts...", Fore.YELLOW)
                            self.info_game()
                            return {}
                        else:
                            response.raise_for_status()

                    # Jika respons tidak sukses meskipun status code OK
                    if not spin_data.get("success", False):
                        message = spin_data.get("message", "")
                        if "Can't spin, get steal target first" in message:
                            self.log("Can't spin, get steal target first. Initiating steal attempts...", Fore.YELLOW)
                            self.info_game()
                            return {}
                        else:
                            raise ValueError("Spin request failed. Check API response: " + message)

                    return spin_data

                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Failed to perform spin: {e}", Fore.RED)
                    try:
                        self.log(f"📄 Response content: {response.text}", Fore.RED)
                    except Exception:
                        pass
                    return {}
                except Exception as e:
                    self.log(f"❗ An unexpected error occurred during spin request: {e}", Fore.RED)
                    try:
                        self.log(f"📄 Response content: {response.text}", Fore.RED)
                    except Exception:
                        pass
                    return {}

            spin_data = perform_spin_request()
            if not spin_data:
                # Jika gagal melakukan spin, lanjutkan ke iterasi berikutnya
                continue

            # 🔍 Phase 2: Memvalidasi dan Memproses Respons Spin
            data = spin_data.get("data", {})
            if not data:
                self.log("❌ Spin data is missing in the response.", Fore.RED)
                continue

            slots = [slot.get("item") for slot in data.get("slots", [])]
            sum_rewards = data.get("sumRewards", [])
            self.log(f"🎲 Slots: {' | '.join(map(str, slots))}", Fore.LIGHTGREEN_EX)

            # Kurangi energy sesuai jumlah spin yang berhasil dilakukan
            self.energy -= spins_to_perform
            self.log(f"⚡ Energy remaining: {self.energy}", Fore.MAGENTA)

            # 🎯 Phase 3: Menangani Hasil Spin
            # Jika dalam salah satu spin terdapat kombinasi tertentu,
            # maka dipanggil fungsi khusus (misal: perform_steal_attempts atau perform_raid).
            if all(slot == 5 for slot in slots):
                self.log("💥 Jackpot! All slots are 5! Initiating steal attempts...", Fore.YELLOW)
                self.perform_steal_attempts()
            elif all(slot == 4 for slot in slots):
                self.log("🛡️ Raid opportunity! All slots are 4! Fetching raid information...", Fore.YELLOW)
                self.perform_raid()
            else:
                if sum_rewards:
                    for reward in sum_rewards:
                        kind = reward.get("kind", "Unknown")
                        reward_type = reward.get("type", "Unknown")
                        amount = reward.get("amount", {}).get("value", 0)
                        self.log(
                            f"💎 Reward: Kind {kind}, Type {reward_type}, Amount: {amount}",
                            Fore.LIGHTGREEN_EX,
                        )
                else:
                    self.log("🎁 No rewards from this spin.", Fore.YELLOW)

    def perform_raid(self) -> None:
        """
        Menangani logika raid ketika semua slot bernilai 4 dalam game.

        Fase dalam raid ini:
        
        🔰 **Phase 0: Mengambil Informasi Raid**
        - Mengambil data raid dari API untuk mendapatkan target user dan otter.
        
        🚀 **Phase 1: Menentukan Target dan Bagian untuk Di-raid**
        - Memilih target part berdasarkan kondisi bagian yang rusak (broken) atau jumlah bintang paling rendah.
        
        🛡️ **Phase 2: Melakukan Raid**
        - Mengirim permintaan raid dengan payload default.
        - Jika raid gagal dan opsi *Golden Punch* tersedia, ulangi proses dengan mengaktifkan *Golden Punch*.
        """
        raid_info_url = f"{self.BASE_URL}v1/game/raid-info"
        raid_url = f"{self.BASE_URL}v1/game/raid"
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

        # 🔰 Phase 0: Mengambil Informasi Raid
        def fetch_raid_info() -> dict:
            self.log("🔍 Fetching raid information...", Fore.CYAN)
            try:
                response = requests.get(raid_info_url, headers=headers)
                response.raise_for_status()
                raid_info = response.json()
                if not raid_info.get("success", False):
                    raise ValueError("Raid info request failed. Check the API response.")
                return raid_info
            except Exception as e:
                self.log(f"❌ Error fetching raid information: {e}", Fore.RED)
                return {}

        # 🚀 Phase 1: Menentukan target raid dan bagian yang akan di-incar
        def determine_target(raid_info: dict) -> (dict, dict):
            try:
                data = raid_info["data"]
                target_user = data["user"]
                target_otter = data["otter"]
                self.log(f"🎯 Target User: {target_user['firstName']}", Fore.LIGHTGREEN_EX)
                self.log(
                    f"🦦 Target Otter Level: {target_otter['level']}, Stars: {target_otter['totalStars']}",
                    Fore.LIGHTGREEN_EX,
                )
                parts = target_otter["parts"]
                broken_parts = [part for part in parts if part["broken"]]
                if broken_parts:
                    target_part = min(broken_parts, key=lambda x: x["stars"])
                else:
                    target_part = min(parts, key=lambda x: x["stars"])
                self.log(
                    f"⚔️ Targeting part: {target_part['type']} (Stars: {target_part['stars']}, Broken: {target_part['broken']})",
                    Fore.YELLOW,
                )
                return target_user, target_part
            except Exception as e:
                self.log(f"❌ Error determining raid target: {e}", Fore.RED)
                return {}, {}

        # 🛡️ Phase 2: Melakukan raid dengan handling untuk Golden Punch jika diperlukan
        def execute_raid(golden_punch: bool = False) -> dict:
            target_info = fetch_raid_info()
            if not target_info:
                return {}
            target_user, target_part = determine_target(target_info)
            if not target_user or not target_part:
                return {}

            raid_payload = {
                "goldenPunch": golden_punch,
                "part": target_part["type"],
                "type": 1,
                "userId": target_user["id"],
            }

            raid_log_prefix = "✨ Initiating Golden Punch raid..." if golden_punch else "⚔️ Initiating raid..."
            self.log(raid_log_prefix, Fore.YELLOW)

            try:
                response = requests.post(raid_url, headers=headers, json=raid_payload)
                response.raise_for_status()
                raid_result = response.json()
                return raid_result
            except Exception as e:
                self.log(f"❌ Error during raid execution: {e}", Fore.RED)
                return {}

        # Eksekusi raid tahap awal (tanpa Golden Punch)
        raid_data = execute_raid(golden_punch=False)
        if not raid_data:
            return

        # Jika raid tidak sukses, cek opsi Golden Punch
        if not raid_data.get("success", False):
            self.log("❌ Raid failed. No rewards obtained.", Fore.RED)
            golden_punch_info = raid_data.get("data", {}).get("goldenPunch", {})
            if golden_punch_info.get("canPunch", False):
                self.log(
                    "✨ Golden Punch is available! Reattempting raid with Golden Punch for efficiency...",
                    Fore.CYAN,
                )
                raid_data = execute_raid(golden_punch=True)
                if raid_data.get("success", False):
                    reward = raid_data["data"]["reward"]
                    self.log(
                        f"🏆 Golden Punch Reward: Kind {reward['kind']}, Type {reward['type']}, Amount: {reward['amount']['value']}",
                        Fore.LIGHTGREEN_EX,
                    )
                else:
                    self.log("❌ Golden Punch raid failed.", Fore.RED)
            return

        # Jika raid sukses, tampilkan reward
        reward = raid_data["data"]["reward"]
        self.log(
            f"🏆 Raid Reward: Kind {reward['kind']}, Type {reward['type']}, Amount: {reward['amount']['value']}",
            Fore.LIGHTGREEN_EX,
        )
    
    def perform_steal_attempts(self) -> None:
        """
        Melakukan hingga 3 percobaan steal (mencuri) dengan memilih posisi secara acak.
        
        Fase dalam steal attempts:
        
        🔰 **Phase 0: Persiapan Awal**
        - Menentukan URL, header, dan inisialisasi variabel untuk menyimpan posisi yang sudah dipakai.
        
        🚀 **Phase 1: Melakukan Percobaan Steal**
        - Melakukan percobaan steal secara acak hingga maksimal 3 kali atau posisi habis digunakan.
        
        🔍 **Phase 2: Menangani Hasil Percobaan**
        - Mengevaluasi respons dari tiap percobaan. Jika berhasil, menampilkan reward.
        - Jika terdapat error terkait limit, menghentikan seluruh percobaan.
        """
        req_url_steal = f"{self.BASE_URL}v1/game/steal"
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

        max_attempts = 3
        attempt_count = 0
        used_positions = set()

        # 🚀 Phase 1: Fungsi inner untuk melakukan satu percobaan steal di posisi tertentu
        def attempt_steal(position: int) -> dict:
            self.log(f"🚀 Attempting to steal at position {position} (Attempt {attempt_count}/{max_attempts})...", Fore.CYAN)
            try:
                response = requests.post(req_url_steal, headers=headers, json={"position": position})
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Request failed: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {response.text if 'response' in locals() else 'No response'}", Fore.RED)
                except Exception:
                    self.log("📄 No response available.", Fore.RED)
                return {}
            except Exception as e:
                self.log(f"❗ An unexpected error occurred: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {response.text if 'response' in locals() else 'No response'}", Fore.RED)
                except Exception:
                    self.log("📄 No response available.", Fore.RED)
                return {}

        # 🚀 Phase 1: Melakukan percobaan hingga maksimal yang diijinkan
        while attempt_count < max_attempts:
            # Jika semua posisi sudah digunakan, hentikan percobaan
            if len(used_positions) >= 5:
                self.log("All positions used, stopping attempts.", Fore.RED)
                break

            position = random.randint(1, 5)
            if position in used_positions:
                continue

            used_positions.add(position)
            attempt_count += 1

            steal_data = attempt_steal(position)
            if not steal_data:
                continue

            # 🔍 Phase 2: Menangani hasil percobaan
            if not steal_data.get("success", False):
                message = steal_data.get("message", "Unknown error")
                self.log(f"⚠️ Steal attempt failed: {message}", Fore.YELLOW)
                # Jika error terkait limit, hentikan seluruh percobaan
                if "limit" in message.lower():
                    self.log("⛔ Limit reached, stopping attempts.", Fore.RED)
                    break
                continue

            # Jika berhasil, cek dan tampilkan reward
            reward = steal_data.get("data", {}).get("reward", {})
            if reward:
                kind = reward.get("kind", "Unknown")
                reward_type = reward.get("type", "Unknown")
                amount = reward.get("amount", {}).get("value", 0)
                self.log(f"💰 Steal Success: Kind {kind}, Type {reward_type}, Amount: {amount}", Fore.LIGHTGREEN_EX)
            else:
                self.log("🎯 Attempt failed: No reward found.", Fore.YELLOW)

        # Jika sudah mencapai maksimal percobaan, tampilkan log informasi
        if attempt_count >= max_attempts:
            self.log("🛑 Maximum number of attempts reached. Stopping.", Fore.RED)

    def quest(self) -> None:
        """Fetches and completes both regular and special quests in distinct phases."""

        def complete_quests(req_url: str, quest_type: str, complete_url: str = None) -> None:
            headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

            def fetch_quest_list():
                """📥 Phase 1: Fetch quest list"""
                self.log(f"📋 Fetching {quest_type} quests list...", Fore.CYAN)
                try:
                    response = requests.get(req_url, headers=headers)
                    response.raise_for_status()
                    quest_data = self.decode_response(response)
                    if not quest_data.get("success", False):
                        self.log(f"⚠️ Failed to fetch {quest_type} quests list.", Fore.YELLOW)
                        return []
                    return quest_data.get("data", {}).get("quests", [])
                except Exception as e:
                    self.log(f"❌ Error while fetching {quest_type} quests: {e}", Fore.RED)
                    return []

            def try_complete_quest(quest):
                """🚀 Phase 2: Try to complete quest"""
                quest_id = quest.get("questID")
                description = quest.get("description", "No description")
                status = quest.get("questStatus")
                if status != 1:
                    return False

                payload = {"questID": quest_id}
                req_url_quest = complete_url or f"{self.BASE_URL}v1/quest/do"
                self.log(f"🗺️ Attempting {quest_type} quest {quest_id} ➜ {description}", Fore.CYAN)

                try:
                    res = requests.post(req_url_quest, headers=headers, json=payload)
                    res.raise_for_status()
                    result = self.decode_response(res)

                    if not result.get("success", False):
                        self.log(f"⚠️ Quest {quest_id} failed to complete.", Fore.YELLOW)
                        return False

                    data = result.get("data", {})
                    quest_done_id = data.get("questDoneID", "Unknown")
                    self.log(f"✅ {quest_type.capitalize()} quest {quest_done_id} completed successfully!", Fore.LIGHTGREEN_EX)

                    # 🎁 Phase 3: Reward handling
                    rewards = data.get("rewards", [])
                    if rewards:
                        self.log(f"🎁 Rewards received:", Fore.LIGHTGREEN_EX)
                        for r in rewards:
                            kind = r.get("kind", "Unknown")
                            reward_type = r.get("type", "Unknown")
                            amount = r.get("amount", {}).get("value", 0)
                            self.log(f"  🪙 {kind} - {reward_type}: {amount}", Fore.GREEN)
                    else:
                        self.log(f"🎁 No rewards for quest {quest_id}.", Fore.YELLOW)
                    return True

                except Exception as e:
                    self.log(f"❌ Failed to complete quest {quest_id}: {e}", Fore.RED)
                    return False

            # 🌀 Phase 0: Execute all phases
            quests = fetch_quest_list()
            if not quests:
                self.log(f"⚠️ No available {quest_type} quests.", Fore.YELLOW)
                return

            self.log(f"🔄 Processing {len(quests)} {quest_type} quests...", Fore.LIGHTMAGENTA_EX)
            completed_count = 0
            for q in quests:
                if try_complete_quest(q):
                    completed_count += 1

            self.log(f"🏁 {completed_count}/{len(quests)} {quest_type} quests completed.\n", Fore.LIGHTBLUE_EX)

        # 🔁 Run for both regular and special quests
        complete_quests(f"{self.BASE_URL}v1/quest", "regular")
        complete_quests(
            req_url=f"{self.BASE_URL}v1/special-quest",
            quest_type="special",
            complete_url=f"{self.BASE_URL}v1/special-quest/do"
        )

    def otter(self) -> None:
        """Fetches Otter details, repairs broken parts, and upgrades parts until no more eligible parts,
        then lists the final Otter details."""
        # Endpoints API
        info_url = f"{self.BASE_URL}v1/otter"
        repair_url = f"{self.BASE_URL}v1/otter/repair"
        upgrade_url = f"{self.BASE_URL}v1/otter/upgrade"
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
        total_medals = 0

        def fetch_otter_info():
            """Helper to fetch and return fresh otter info."""
            res = requests.get(info_url, headers=headers)
            res.raise_for_status()
            data = self.decode_response(res)
            if not data.get("success", False):
                raise Exception("Failed to fetch Otter info")
            return data["data"]

        try:
            self.log("🐾 Fetching Otter details...", Fore.CYAN)
            otter = fetch_otter_info()
            self.log(
                f"🦦 Otter Level: {otter.get('level', 0)} | Total Stars: {otter.get('totalStars', 0)}",
                Fore.LIGHTGREEN_EX,
            )

            # Set untuk menyimpan part yang tidak bisa diperbaiki (misal error 500)
            non_repairable_parts = set()

            # --- Repair Phase ---
            # Repair eligible: part yang rusak, yaitu broken == true
            while True:
                otter = fetch_otter_info()  # Refresh info setiap iterasi
                parts = otter.get("parts", [])
                repairable_parts = [
                    p for p in parts 
                    if (p.get("broken", False) is True) and (p.get("type") not in non_repairable_parts)
                ]
                if not repairable_parts:
                    self.log("✅ No parts need repair or all are marked non-repairable. Exiting repair phase.", Fore.LIGHTGREEN_EX)
                    break

                any_repaired = False
                for part in repairable_parts:
                    part_type = part.get("type")
                    self.log(f"🔧 Repairing part: {part_type}", Fore.YELLOW)
                    try:
                        res = requests.post(repair_url, headers=headers, json={"part": part_type})
                        res.raise_for_status()
                        data = self.decode_response(res)
                        if data.get("success", False):
                            self.log("✅ Repair successful!", Fore.LIGHTGREEN_EX)
                            any_repaired = True
                        else:
                            self.log(f"❌ Repair failed: {data.get('message', 'Unknown')}", Fore.RED)
                            if res.status_code == 500:
                                non_repairable_parts.add(part_type)
                        otter = fetch_otter_info()  # Refresh setelah percobaan repair
                    except Exception as e:
                        self.log(f"❌ Repair error: {e}", Fore.RED)
                        if "500" in str(e):
                            non_repairable_parts.add(part_type)
                        otter = fetch_otter_info()
                if not any_repaired:
                    self.log("❗ No successful repairs in this iteration. Exiting repair phase.", Fore.YELLOW)
                    break

            # --- Upgrade Phase ---
            # Upgrade eligible: part yang tidak rusak (broken == false) dan stars kurang dari 3
            while True:
                otter = fetch_otter_info()  # Refresh info setiap iterasi
                upgraded_any = False
                parts = otter.get("parts", [])
                for part in parts:
                    part_type = part.get("type")
                    stars = part.get("stars", 0)
                    if part.get("broken", False) is True or stars >= 3:
                        # Jika part rusak, jangan upgrade. Upgrade hanya untuk part yang tidak rusak.
                        continue

                    self.log(f"⬆️ Upgrading part: {part_type}", Fore.CYAN)
                    try:
                        res = requests.post(upgrade_url, headers=headers, json={"part": part_type})
                        res.raise_for_status()
                        data = self.decode_response(res)
                        if data.get("success", False):
                            medal = data.get("data", {}).get("medal", 0)
                            total_medals += medal
                            self.log(
                                f"🏅 Upgrade successful! +{medal} medals (Total: {total_medals})",
                                Fore.LIGHTGREEN_EX,
                            )
                            upgraded_any = True
                        else:
                            msg = data.get("message", "").lower()
                            if "not enough coins" in msg:
                                self.log("💰 Not enough coins to upgrade.", Fore.RED)
                            else:
                                self.log(f"❌ Upgrade failed: {msg}", Fore.RED)
                        otter = fetch_otter_info()  # Refresh setelah setiap upgrade attempt
                    except Exception as e:
                        self.log(f"❌ Upgrade error: {e}", Fore.RED)
                        otter = fetch_otter_info()
                if not upgraded_any:
                    self.log("✅ No parts eligible for upgrade. Exiting upgrade phase.", Fore.LIGHTGREEN_EX)
                    break

            # Final Refresh untuk menampilkan status terakhir
            otter = fetch_otter_info()
            self.log("✅ All possible upgrades and repairs completed.", Fore.LIGHTMAGENTA_EX)
            self.log(
                f"🦦 Final Otter Level: {otter.get('level', 0)} | Total Stars: {otter.get('totalStars', 0)}",
                Fore.LIGHTGREEN_EX,
            )

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Network error: {e}", Fore.RED)
        except Exception as e:
            self.log(f"❗ Unexpected error: {e}", Fore.RED)

    def buy(self, type: str = "gold") -> None:
        """Handles purchase operations in the Otter game.

        Args:
            type (str): The type of item to buy. Defaults to 'gold'.
        """
        shop_url = f"{self.BASE_URL}v1/shop/buy-currency"
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

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
                self.log(
                    f"❌ Purchase failed. Message: {response_data.get('message', 'No message provided.')}",
                    Fore.RED,
                )
                return

            self.log(f"✅ Successfully purchased {type}.", Fore.LIGHTGREEN_EX)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to perform Otter operations: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error during Otter operations: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(
                f"❗ An unexpected error occurred during Otter operations: {e}",
                Fore.RED,
            )
            self.log(f"📄 Response content: {response.text}", Fore.RED)

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]

async def process_account(account, original_index, account_label, otter, config):

    ua = UserAgent()
    otter.HEADERS["user-agent"] = ua.random

    # Menampilkan informasi akun
    display_account = account[:10] + "..." if len(account) > 10 else account
    otter.log(f"👤 Processing {account_label}: {display_account}", Fore.YELLOW)

    # Override proxy jika diaktifkan
    if config.get("proxy", False):
        otter.override_requests()
    else:
        otter.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

    # Login (fungsi blocking, dijalankan di thread terpisah) dengan menggunakan index asli (integer)
    await asyncio.to_thread(otter.login, original_index)

    otter.log("🛠️ Starting task execution...", Fore.CYAN)
    tasks_config = {
        "buy": "💰 Purchase Items",
        "spin": "🎰 Spin the Wheel",
        "quest": "📜 Quest Solver",
        "otter": "🦦 Otter Manager",
    }

    for task_key, task_name in tasks_config.items():
        task_status = config.get(task_key, False)
        color = Fore.YELLOW if task_status else Fore.RED
        otter.log(
            f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
            color,
        )
        if task_status:
            otter.log(f"🔄 Executing {task_name}...", Fore.CYAN)
            await asyncio.to_thread(getattr(otter, task_key))

    delay_switch = config.get("delay_account_switch", 10)
    otter.log(
        f"➡️ Finished processing {account_label}. Waiting {Fore.WHITE}{delay_switch}{Fore.CYAN} seconds before next account.",
        Fore.CYAN,
    )
    await asyncio.sleep(delay_switch)


async def worker(worker_id, otter, config, queue):
    """
    Setiap worker akan mengambil satu akun dari antrian dan memprosesnya secara berurutan.
    Worker tidak akan mengambil akun baru sebelum akun sebelumnya selesai diproses.
    """
    while True:
        try:
            original_index, account = queue.get_nowait()
        except asyncio.QueueEmpty:
            break
        account_label = f"Worker-{worker_id} Account-{original_index+1}"
        await process_account(account, original_index, account_label, otter, config)
        queue.task_done()
    otter.log(f"Worker-{worker_id} finished processing all assigned accounts.", Fore.CYAN)


async def main():
    otter = otterloot()  
    config = otter.load_config()
    all_accounts = otter.query_list
    num_threads = config.get("thread", 1)  # Jumlah worker sesuai konfigurasi

    if config.get("proxy", False):
        proxies = otter.load_proxies()

    otter.log(
        "🎉 [LIVEXORDS] === Welcome to Otter Loot Automation === [LIVEXORDS]", Fore.YELLOW
    )
    otter.log(f"📂 Loaded {len(all_accounts)} accounts from query list.", Fore.YELLOW)

    while True:
        # Buat queue baru dan masukkan semua akun (dengan index asli)
        queue = asyncio.Queue()
        for idx, account in enumerate(all_accounts):
            queue.put_nowait((idx, account))

        # Buat task worker sesuai dengan jumlah thread yang diinginkan
        workers = [
            asyncio.create_task(worker(i + 1, otter, config, queue))
            for i in range(num_threads)
        ]

        # Tunggu hingga semua akun di queue telah diproses
        await queue.join()

        # Opsional: batalkan task worker (agar tidak terjadi tumpang tindih)
        for w in workers:
            w.cancel()

        otter.log("🔁 All accounts processed. Restarting loop.", Fore.CYAN)
        delay_loop = config.get("delay_loop", 30)
        otter.log(
            f"⏳ Sleeping for {Fore.WHITE}{delay_loop}{Fore.CYAN} seconds before restarting.",
            Fore.CYAN,
        )
        await asyncio.sleep(delay_loop)


if __name__ == "__main__":
    asyncio.run(main())