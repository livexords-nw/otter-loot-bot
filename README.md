---

<h1 align="center">Otter Loot Bot</h1>

<p align="center">Automate tasks in Otter Loot to enhance your efficiency and maximize your results!</p>

---

## 🚀 **About the Bot**

The Otter Loot Bot is designed to automate various tasks in **Otter Loot**, including:

- **Automatic Spin**
- **Automatic Quest Completion**
- **Automatic Otter Management**
- **Multi-Account Support**
- **Delay Loop and Account Switching**

With this bot, you can save time and maximize your outcomes without manual interactions.

---

## 🌟 **Version v1.0.1**

### 🔄 **Updates**
- **Bug Fix:** Improved the logic for the steal feature to handle the following:
  - Stops attempts if the error is related to request limits.
  - Continues retrying if the error is related to the target.
  - Avoids reusing positions that have already been attempted.
- Enhanced randomization for steal positions, now ranging from 1 to 10.
- Added a maximum error limit to prevent infinite loops during failed attempts.

### 🐛 **Bug Fix Details**
- Fixed an issue where the steal process would retry the same positions multiple times.
- Resolved a problem where the steal process did not properly handle error responses from the server, leading to unintended behaviors.
- Optimized error handling for better user feedback and smoother execution.

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

| **Function**           | **Description**                          | **Default** |
| ---------------------- | ---------------------------------------- | ----------- |
| `spin`                 | Automate spin actions                    | `True`      |
| `quest`                | Complete quests automatically            | `True`      |
| `otter`                | Manage Otter tasks automatically         | `True`      |
| `delay_account_switch` | Delay between account switches (seconds) | `10`        |
| `delay_loop`           | Delay before the next loop (seconds)     | `3000`      |

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
