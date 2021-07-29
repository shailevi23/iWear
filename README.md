<img src="https://user-images.githubusercontent.com/58184521/121235257-54058280-c89d-11eb-9613-1590a2396d57.png" width="750">

# Description
iWear goal is to bring people’s closet to the digital world and make its usage advanced and smarter.  
iWear is a web-app, using RFID technology iWear monitors and analyzes the use of the user's clothing items and provides statistics and data.  
Based on the statistics and data, the user can manage his closet and get recommendations of clothing items based on different parameters.

iWear developed in Python with Django in a Linux environment with VM.

# Motivation
Technology is advancing and spreading in all areas including the fashion world, but the one who was left behind is the closet which we all use on a daily basis.  
Nowadays, New clothes trends and ethics are rising and changing very often. Today’s generation focuses more than ever on people's appearance, how they look like and what they are wearing.  
One needs to spend time and effort to stay updated and relevant to the fashion trends. People spending a lot of time searching for the best clothing items for their specific dressing style.  
In addition, People manage their closet, according to gut feelings. Thinking they suffer a lack of products from some clothing category when in fact they have a lot of items that have not been worn often.  
iWear system aspires to solve the needs mentioned above.  
iWear seeing itself as a part of the global digital revolution, especially in the field of smart homes.

# How iWear works:
Initial installation of an RFID-Reader (user-unique) in a "strategic" location in the user home, such as the home door entrance.  
Couple the tag and the clothing item himself.  (the tags Durable for heat, laundry, ironing, etc.)  
Now, the iWear system is ready to go and the reader is ready for action.  
Every time the user passes by the reader while wearing a clothing item, the reader will identify the item and save a worn event with the relevant information in the system.

# Screenshots
## My closet
<img src="https://user-images.githubusercontent.com/58184521/127578118-37493bb5-2bcf-466f-b345-8a668efbf591.png" width="650" />

## Category overview
<img src="https://user-images.githubusercontent.com/58184521/127578200-77b7b33c-611f-49d2-a848-f8f7dac702c0.png" width="650" />

## Clothing item overview
<img src="https://user-images.githubusercontent.com/58184521/127578050-148163b1-fc38-42df-8419-ab803c7e44a2.png" width="650" />

# Features
- Account creation & management.
- Add and manage clothing items.
- Capture information about the use of clothing items. including weather temperature.
- Closet/Category/Item overview.
- Intelligent recommendations based on:  
&nbsp;&nbsp; * Clothing category.  
&nbsp;&nbsp; * Weather temperature.  
&nbsp;&nbsp; * Random parameters.
- Fully functional ADMIN site.

# Architecture
| Frontend      | Backennd      | Datebase      |
| ------------- | ------------- | ------------- |
| HTML          | Python        | SQLite        |
| CSS           | Django        |  
| JavaScript    | Vagrant       |
| Bootstarp     |


# Installation
1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)/[VMWare](https://www.vmware.com/) hypervisor.
2. Clone [roo.me](https://github.com/beyond-io/roo.me) repository.
   ```sh
   https://github.com/AmitAharoni/iWear2021.git
   ```
3. Open any terminal and navigate to the project directory.
4. Run the `vagrant up` command.
5. Use any browser and navigate to - `http://127.0.0.1:8000` (localhost).
6. Install and connect the RFID reader (OR RUN MANUALLY).
