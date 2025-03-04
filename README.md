---

<h1 align="center">Otter Loot Bot</h1>

<p align="center">Automate tasks in Otter Loot to enhance your efficiency and maximize your results!</p>

---

## 🚀 **About the Bot**

The Otter Loot Bot is designed to automate various tasks in **Otter Loot**, including:

- **Automatic Spin**
- **Automatic Quest Completion**
- **Automatic Otter Management**
- **Automatic Purchase Packs**
- **Multi-Account Support**
- **Delay Loop and Account Switching**
- **Proxy Support**

With this bot, you can save time and maximize your outcomes without manual interactions.

---

## 🌟 **Version v1.1.5**

### 🔄 **Updates**

1. Optimized the spin system.
2. Optimized the steal system.
3. Optimized the raid system.
4. Added proxy support as a bot feature.
5. Updated configuration file (`config.json`).

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

Below is the updated configuration file. Adjust these settings as needed:

```json
{
  "spin": true,
  "quest": true,
  "otter": true,
  "buy": true,
  "proxy": false,
  "type_buy": "energy",
  "delay_loop": 3000,
  "delay_account_switch": 10
}
```

| **Function**           | **Description**                                      | **Default** |
| ---------------------- | ---------------------------------------------------- | ----------- |
| `spin`                 | Automate spin actions                                | `true`      |
| `quest`                | Complete quests automatically                        | `true`      |
| `otter`                | Manage Otter tasks automatically                     | `true`      |
| `buy`                  | Enable or disable buy functionality                  | `true`      |
| `proxy`                | Enable or disable proxy support                      | `false`     |
| `type_buy`             | Specify the type of item to buy (`gold` or `energy`) | `energy`    |
| `delay_loop`           | Delay before the next loop (seconds)                 | `3000`      |
| `delay_account_switch` | Delay between account switches (seconds)             | `10`        |

---

## 📚 **Installation Steps**

1. **Clone the Repository**  
   Copy the project to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/otter-loot-bot.git
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

5. **Set Up Proxy (Optional)**  
   To use a proxy, create a `proxy.txt` file and add proxies in the format:

   ```
   http://username:password@ip:port
   ```

   - Only HTTP and HTTPS proxies are supported.

6. **Run the Bot**  
   Execute the bot using the following command:

   ```bash
   python main.py
   ```

---

## 🚀 **Key Features Overview**

- **Auto Spin**: Automatically perform spin actions.
- **Auto Quest Completion**: Complete quests without manual effort.
- **Auto Otter Management**: Optimize and manage Otters seamlessly.
- **Auto Buy Pack**: Automatically purchase packs.
- **Multi-Account Support**: Run multiple accounts simultaneously.
- **Delay Loop and Account Switching**: Set intervals for looping and account transitions.
- **Proxy Support**: Optionally route your requests through proxies by enabling the feature in `config.json` and providing proxy details in `proxy.txt`.

---

## 🛠️ **Contributing**

This project is developed by **LIVEXORDS**. If you have suggestions, questions, or would like to contribute, feel free to contact us:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=LIVEXORDS&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---
