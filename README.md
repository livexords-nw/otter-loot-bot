---

<h1 align="center">Otter Loot Bot</h1>

<p align="center">Automate tasks in Otter Loot to enhance your efficiency and maximize your results!</p>

---

## 🚀 **About the Bot**

The Otter Loot Bot is designed to automate various tasks in **Otter Loot**, including:

- **Automatic Spin**
- **Automatic Quest Completion**
- **Automatic Otter Management**
- **Automatic purchase packs**
- **Multi-Account Support**
- **Delay Loop and Account Switching**

With this bot, you can save time and maximize your outcomes without manual interactions.

---

## 🌟 **Version v1.1.2**

### 🔄 **Updates**

- **Feature Enhancement:** Improved the `Otter Manager` functionality:
  - Ensures all part types are processed sequentially without skipping.
  - Added more detailed logging to track:
    - Repairs for broken parts.
    - Upgrade attempts, including reasons for failures (e.g., insufficient coins).
    - Successes, medals earned, and overall progress.
  - Implements continuous processing until all parts are either repaired or upgraded to the maximum allowed level.
- **Code Optimization:** Enhanced error-handling mechanisms for better resilience against server-side errors and invalid responses.
- **Raid System:** Added support for the Golden Punch feature, including automatic re-fetching of raid information when necessary.
- **Steal Mechanism:** Improved the steal system for better handling of target selection and raid logic.
- **Purchase Feature:** Introduced a feature to buy gold or energy, configurable via the `type_buy` option, with enhanced logging and error handling.
- **Detailed Logging:** Added new loggers in various sections to provide better insights and debugging capabilities during operations.

### 🛠️ **Bug Fix Details**

- Resolved an issue where the process would stop prematurely if an error occurred during the repair or upgrade of a part.
- Fixed potential errors in the raid system when processing targets with incomplete data.
- Improved log readability for easier debugging and monitoring of Otter operations.

---

## 📥 **How to Register**

Start using Otter Loot by registering through the following link:

<div align="center">
  <a href="https://t.me/otterlootbot?start=ref_6777e44f0fcc137ad0987ea9" target="_blank">
    <img src="https://img.shields.io/static/v1?message=OtterLoot&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---

## ⚙️ **Configuration in `config.json`**

| **Function**           | **Description**                                      | **Default** |
| ---------------------- | ---------------------------------------------------- | ----------- |
| `spin`                 | Automate spin actions                                | `True`      |
| `quest`                | Complete quests automatically                        | `True`      |
| `otter`                | Manage Otter tasks automatically                     | `True`      |
| `delay_account_switch` | Delay between account switches (seconds)             | `10`        |
| `delay_loop`           | Delay before the next loop (seconds)                 | `3000`      |
| `buy`                  | Enable or disable buy functionality                  | `False`     |
| `type_buy`             | Specify the type of item to buy (`gold` or `energy`) | `gold`      |

---

## 📚 **Installation Steps**

1. **Clone the Repository**  
   Copy the project to your local machine:

   ```bash
   git clone https://github.com/username/otter-loot-bot.git
   ```

2. **Navigate to the Project Folder**  
   Move to the project directory:

   ```bash
   cd otter-loot-bot
   ```

3. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Query**  
   Create a `query.txt` file and add your Otter Loot query data.

5. **Run the Bot**  
   Execute the bot using the following command:

   ```bash
   python main.py
   ```

---

## 🚀 **Key Features Overview**

- **Auto Spin**: Automatically perform spin actions.
- **Auto Quest Completion**: Complete quests without manual effort.
- **Auto Otter Management**: Optimize and manage Otters seamlessly.
- **Auto buy Pack**: Automatically purchase packs.
- **Multi-Account Support**: Run multiple accounts simultaneously.
- **Delay Loop and Account Switching**: Set intervals for looping and account transitions.

---

## 🛠️ **Contributing**

This project is developed by **LIVEXORDS**. If you have suggestions, questions, or would like to contribute, feel free to contact us:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=LIVEXORDS&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---
