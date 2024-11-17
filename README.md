Trade-Corp Platform
Description
Trade-corp Platform is a web application that allows users to trade virtual skins from games such as CS2 and Valorant. Users can:
• Offer trades to other users.
• Accept trade offers.
• View available trade offers in real time.
Functionality
• User registration and authorization.
• Create trades (exchange skins between users).
• View available trades for senders and receivers.
• Manage user skin inventory.
• Trade logic with automatic inventory update.
Technologies used
• Backend: Flask (Python)
• Frontend: HTML, CSS, Jinja2
• Database: MySQL

In order for everything to work for you, you first need to insert these codes into your empty mysql databaseCreate database:


CREATE TABLE users ( user_id int NOT NULL AUTO_INCREMENT, username varchar(255) NOT NULL, email varchar(255) NOT NULL, balance int DEFAULT '0', password varchar(255) NOT NULL, PRIMARY KEY (user_id), UNIQUE KEY email (email) ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE valskins ( id int NOT NULL AUTO_INCREMENT, picture varchar(255) NOT NULL, cost varchar(255) NOT NULL, release_date date NOT NULL, description text NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE cs2skins ( id int NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL, picture varchar(255) DEFAULT NULL, cost int DEFAULT NULL, release_date date DEFAULT NULL, description text, PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE trade_offers ( offer_id int NOT NULL AUTO_INCREMENT, user_id_from int NOT NULL, skin_id_from int NOT NULL, user_id_to int NOT NULL, skin_id_to int NOT NULL, status enum('pending','accepted','rejected') DEFAULT 'pending', trade_date timestamp NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (offer_id), KEY user_id_from (user_id_from), KEY user_id_to (user_id_to), KEY skin_id_from (skin_id_from), KEY skin_id_to (skin_id_to), CONSTRAINT trade_offers_ibfk_1 FOREIGN KEY (user_id_from) REFERENCES users (user_id), CONSTRAINT trade_offers_ibfk_2 FOREIGN KEY (user_id_to) REFERENCES users (user_id), CONSTRAINT trade_offers_ibfk_3 FOREIGN KEY (skin_id_from) REFERENCES user_inventory (skin_id), CONSTRAINT trade_offers_ibfk_4 FOREIGN KEY (skin_id_to) REFERENCES user_inventory (skin_id) ) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE trade_offers ( offer_id int NOT NULL AUTO_INCREMENT, user_id_from int NOT NULL, skin_id_from int NOT NULL, user_id_to int NOT NULL, skin_id_to int NOT NULL, status enum('pending','accepted','rejected') DEFAULT 'pending', trade_date timestamp NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (offer_id), KEY user_id_from (user_id_from), KEY user_id_to (user_id_to), KEY skin_id_from (skin_id_from), KEY skin_id_to (skin_id_to), CONSTRAINT trade_offers_ibfk_1 FOREIGN KEY (user_id_from) REFERENCES users (user_id), CONSTRAINT trade_offers_ibfk_2 FOREIGN KEY (user_id_to) REFERENCES users (user_id), CONSTRAINT trade_offers_ibfk_3 FOREIGN KEY (skin_id_from) REFERENCES user_inventory (skin_id), CONSTRAINT trade_offers_ibfk_4 FOREIGN KEY (skin_id_to) REFERENCES user_inventory (skin_id) ) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE user_inventory ( inventory_id int NOT NULL AUTO_INCREMENT, user_id int NOT NULL, skin_id int NOT NULL, game enum('Valorant','CS2') NOT NULL, PRIMARY KEY (inventory_id), KEY user_id (user_id), KEY idx_skin_id (skin_id), CONSTRAINT user_inventory_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (user_id) ) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci



                                          Create cs2 skins:


INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('StatTrak™ Glock-18 | Wasteland Rebel (Factory New)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposbaqKAxf0Ob3djFN79eJg4GYg_L4MrXVqXlU6sB9teXI8oThxlaxqhE_ZGj6I9OccFQ3YwmE-1C5x-u61sC0tM7JwSAy6ydx4XqOnxepwUYbufdxgq4', 3280.90, '2016-06-15', 'Glock-18 | Wasteland Rebel was added to the game on June 15, 2016, as part of The Gamma Collection, which was released alongside the “Gamma Exposure” update. The skin was created by SA_22.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('M4A1-S | Black Lotus (Field-Tested)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhz2v_Nfz5H_uO7wIHahMj2P7rSnVRd59FkmdbM8Ij8nVn6_0BuZG2iI4GUdgBsM1qCrgO2xee5g5Lv6Z_NzCdm7nVw7HbbzUew1QYMMLJUROUd5w', 1000.28, '2022-05-11', 'With a smaller magazine than its unmuffled counterpart, the silenced M4A1 provides quieter shots with less recoil and better accuracy. It has been custom painted with a black lotus flower over a blue and purple base. Adds 2 kills during rifle round, then is discarded
The Kilowatt Collection');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('Souvenir G3SG1 | Safari Mesh (Field-Tested)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposem2LFZfwOP3fDhR5OOilY60mvLwOq7c2G1SsZ0oi7jHrdWs3Vbi_hVtZm3xIYCXJFdrYF_Q_QC8xey9hsLvuMjXiSw0vA346cw', 1150.42, '2013-11-27', 'G3SG1 | Safari Mesh was added to the game on November 27, 2013, as part of The Mirage Collection, which was released alongside the “Out with the old, in with the new” update.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('StatTrak™ Desert Eagle | Trigger Discipline (Field-Tested)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PDdTjlH7duJgJKCkPDxIYTVn3hS4dV9g-fEyoHwjF2hpl1uam-mcoeVIFNoYVGB_gTow7zqgsS1v5TJzHpq7HUrs3bZyxCwg0wdcKUx0iHm0tj7', 1151.44, '2021-05-3', 'Desert Eagle | Trigger Discipline was added to the game on May 3, 2021, as part of The Snakebite Collection, which was released alongside The End of Broken Fang update. The skin was created by moonfighter.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('AWP | Fever Dream (Minimal Wear)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJS_8W1nI-bluP8DLfYkWNFpsAh3bjE8Nqi2QLl_xdtYz3xcYCRc1I2MwzV_gK-yL-7jZfovZjNynR9-n5190ooeH8', 1401, '2016-01-22', 'AWP | Fever Dream appeared in the Workshop on January 22, 2016, and was added to the game on March 15, 2017, as part of The Spectrum Collection, which was released alongside the “Take a trip to the Canals” update. The skin was created by Apel.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('MAC-10 | Amber Fade (Field-Tested)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou7umeldf0vL3dzxG6eO7kZSKm_v9MITck29Y_cg_27qY99v23ATk_RZlZm2gcdeXdwQ8N1DU_VTqxOvm05a-6MzIznZksz5iuyjG2xkMAQ', 1403.03, '2013-11-27', 'MAC-10 | Amber Fade was added to the game on November 27, 2013, as part of The Mirage Collection, which was released alongside the “Out with the old, in with the new” update.  ');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('AWP | Fever Dream (Battle-Scarred)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJS_8W1nI-bluP8DLPUl31IppchjuvA8d6kjADkr0Y_YDz2d9SVelVtaFnV_lC-x-a-hsK8uMnAn3t9-n51dsOtTHk', 2500.70, '2016-01-22', 'AWP | Fever Dream appeared in the Workshop on January 22, 2016, and was added to the game on March 15, 2017, as part of The Spectrum Collection, which was released alongside the “Take a trip to the Canals” update. The skin was created by Apel.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('M4A4 | Desolate Space (Field-Tested)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhjxszFJTwW09izh4-HluPxDKjBl2hU18l4jeHVu4qt2FDsqERoMW7zIIOVIwc2YljQqQW2wenqhZ_vv8-Yn3BruiIh5i3D30vgBg2yDLA', 2535.19, '2020-02-13', 'The M4A4 | Desolate Space was released in 2020. This skin features a desolate, space-like theme and comes with a unique digital camo pattern. It is a popular choice for those who want a space-themed weapon skin.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('P90 | Teardown (Minimal Wear)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpopuP1FBRw7P7NYjV95NOiq4GFk8j3PLfVqWdY781lxOuQ8Nug0VG3_EVkYmz7LIXHJAVrY1HT-FC7lO3ngJ7p7czJznRg6CE8pSGK_1A-hqA', 4565.16, '2021-04-11', 'The P90 | Teardown skin was released as part of the new “Teardown” collection. The design features intricate mechanical parts, giving the skin a teardown look with exposed components and a sleek metallic feel.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('MP7 | Skulls (Field-Tested)', 'https://screenshots.cs.money/csmoney2/e14755e0f90e1b98d68f80fc36a17c5f_large_preview.png', 2503.74, '2022-06-20', 'MP7 | Skulls is a skin designed with a spooky skull motif. Released as part of a Halloween update, it features a unique skull design and vivid colors that pop, making it one of the most iconic skins.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('AK-47 | Neon Revolution (Minimal Wear)', 'https://screenshots.cs.money/csmoney2/77c24eb8599ce7b6d9db3addd304555b_large_preview.png', 3347.79, '2020-08-01', 'The AK-47 | Neon Revolution was added as part of a limited edition skin collection. This vibrant, neon-colored skin features futuristic lines and patterns, making it a popular skin choice for players who like bright, eye-catching designs.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('SG 553 | Damascus Steel (Field-Tested)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpopb3wflFf0uL3dTxP7c-1gZO0hPChZujum25V4dB8xOvAo9nw0AO380ZvZmv2ddWTIVQ2YFnR-FbtwOrtjZPq6ZTPmCZm6HE8pSGK0MwUZ2o', 2536.20, '2015-11-16', 'SG 553 | Damascus Steel is part of the Damascus Collection and features a finely detailed Damascus steel pattern. Released in November 2015, the skin became a fan-favorite due to its unique aesthetic and steel-like finish.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('Galil AR | Sugar Rush (Field-Tested)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposbupIgthwczLZAJF7dC_mL-IlvnwKrjZl2RC18h0juDU-MKh0FHl-ERpZDj6JIWRJg46Zw2C-gW6lLvnhMDo7puczSNguHYltH7fgVXp1pRLVkNX', 3744.45, '2020-11-14', 'Galil AR | Sugar Rush was designed with a playful candy-colored theme. This skin became a favorite among players who enjoy colorful, light-hearted designs, featuring bright shades of pink, purple, and blue.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('UMP-45 | Blaze (Minimal Wear)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpoo7e1f1Jf0vL3dzFD4dmlq4yCkP_gfeuCxTMG7pFw2uiV9I-jjlHi-0dvZDygLY-dJw89NQ3QqFK3lOe9jcSi_MOeUg1XNk4', 4405.89, '2020-07-05', 'UMP-45 | Blaze is part of the “Inferno” skin series. The skin features a fiery red and yellow design, giving the impression of flames enveloping the weapon. It was a popular choice due to its bold, fiery look.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('P90 | Death by Kitty (Minimal Wear)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpopuP1FAR17PDJZS5J-dC6h7-bzqfLP7LWnn8fu8Ek2bmUpIqn0Qy1_0U5NWqlcoGWJwQ7NAzT-VHtkL3u057quM7Oy2wj5HelK5nxRg', 4382.56, '2021-01-10', 'P90 | Death by Kitty was introduced as part of a fun collaboration. The skin features a cute cat-themed design with cartoonish details, making it one of the most popular choices for players who want a whimsical look.');

INSERT INTO cs2skins (Name, picture, cost, release_date, description)
VALUES ('FAMAS | Pulse (Minimal Wear)', 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposLuoKhRf0Ob3dzxP7c-JhJWHhPLLP7LWnn8fvpR13OyTpoig0FK3_kJlN2nzJoSdewE3Y1vV-QS2wOjmg8W0u52am2wj5Hfew1TjOw', 2637.65, '2019-12-30', 'FAMAS | Pulse is part of a high-tech series of weapon skins. Featuring bright neon lines and a futuristic theme, this skin appeals to players who love modern designs.');





                                Create valskins:





INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Prelude to Chaos Stinger', 'https://valorantstrike.com/wp-content/uploads/Valorant-Prelude-to-Chaos-Collection-Stinger-HD.jpg', 1433.32, '2022-06-22', 'The Valorant Prelude to Chaos Stinger is part of the Prelude to Chaos Collection and part of a five skin bundle released on June 22nd 2022. The full set includes the melee blade, Shorty pistol, Stinger, Vandal and Operator. Set in a striking purple, black and gold, the weapons are distinctive and detailed, each coming with three variants.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Prime Vandal', 'https://valorantstrike.com/wp-content/uploads/2020/06/Valorant-Prime-Vandal-hd.jpg', 4678.9, '2021-03-02', 'The Prime Vandal is part of the popular Prime collection in Valorant, featuring a sleek white, blue, and gold finish. It also has multiple variants for further customization.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Elderflame Operator', 'https://valorantstrike.com/wp-content/uploads/2020/07/Valorant-Elderflame-Collection-Operator-HD.jpg', 2499.99, '2020-07-10', 'The Elderflame Operator is part of the Elderflame Collection, a fiery, animated skin that transforms the weapon into a dragon with custom animations.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Oni Phantom', 'https://valorantstrike.com/wp-content/uploads/2020/07/Valorant-Oni-Collection-Phantom-HD.jpg', 1700.25, '2020-08-14', 'The Oni Phantom is part of the Oni Collection, inspired by Japanese folklore, featuring a mystical design and a set of mesmerizing sound effects.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Reaver Vandal', 'https://valorantstrike.com/wp-content/uploads/2020/10/Valorant-Reaver-Collection-Vandal-HD.jpg', 1775.00, '2020-10-27', 'The Reaver Vandal is part of the Reaver Collection, known for its dark and ominous look with a shadowy mist and haunting sound effects.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Glitchpop Judge', 'https://valorantstrike.com/wp-content/uploads/2020/08/Valorant-Glitchpop-Collection-Judge-HD.jpg', 2150.00, '2021-02-02', 'The Glitchpop Judge is part of the Glitchpop Collection, with a cyberpunk aesthetic and bright neon colors.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Forsaken Operator', 'https://valorantstrike.com/wp-content/uploads/2021/04/Valorant-Foresaken-Collection-Operator-HD.jpg', 2000.75, '2021-06-08', 'The Forsaken Operator is part of the Forsaken Collection, featuring an eerie green glow and intricate detailing.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Sentinels of Light Sheriff', 'https://valorantstrike.com/wp-content/uploads/2021/07/Valorant-Sentinels-of-Light-Collection-Sheriff-HD.jpg', 3600.55, '2021-07-22', 'The Sentinels of Light Sheriff is part of the Sentinels of Light Collection, inspired by the battle between light and darkness.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Spline Phantom', 'https://valorantstrike.com/wp-content/uploads/2020/09/Valorant-Spline-Collection-Phantom-HD.jpg', 1850.20, '2020-09-02', 'The Spline Phantom is a unique part of the Spline Collection, with organic, flowing forms and a metallic sheen.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Magepunk Ghost', 'https://valorantstrike.com/wp-content/uploads/2021/04/Valorant-Magepunk-Collection-Ghost-HD.jpg', 1600.00, '2021-04-01', 'The Magepunk Ghost is part of the Magepunk Collection, with steampunk-inspired design and electric blue accents.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('RGX 11Z Pro Classic', 'https://valorantstrike.com/wp-content/uploads/Valorant-RGX-11z-Pro-2-Collection-Classic-HD.jpg', 1550.99, '2021-10-06', 'The RGX 11Z Pro Classic is part of the RGX 11Z Pro Collection, featuring LED lights and a sleek futuristic look.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Sovereign Marshal', 'https://valorantstrike.com/wp-content/uploads/2020/06/Valorant-Sovereign-Marshal-HD.jpg', 1250.00, '2020-05-15', 'The Sovereign Marshal is part of the Sovereign Collection, with a regal gold and white theme, and an ethereal sound.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Nebula Ares', 'https://valorantstrike.com/wp-content/uploads/2020/08/Valorant-Nebula-Collection-Ares-HD.jpg', 1800.50, '2021-01-19', 'The Nebula Ares is part of the Nebula Collection, with a cosmic, space-like theme that makes it stand out.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Winterwunderland Vandal', 'https://valorantstrike.com/wp-content/uploads/2020/12/Valorant-Winterwunderland-Collection-Vandal-HD.jpg', 1400.70, '2020-12-07', 'The Winterwunderland Vandal is part of the Winterwunderland Collection, featuring a winter landscape inside the gun.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Ion Phantom', 'https://valorantstrike.com/wp-content/uploads/2021/07/Valorant-Ruination-Collection-Phantom-HD.jpg', 1700.33, '2020-11-11', 'The Ion Phantom is part of the Ion Collection, featuring a futuristic white and blue energy theme with unique sound effects.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Prime 2.0 Odin', 'https://valorantstrike.com/wp-content/uploads/2021/03/Valorant-Prime-2-Collection-Odin-HD.jpg', 1850.95, '2021-03-02', 'The Prime 2.0 Odin is a part of the Prime 2.0 Collection, featuring a powerful and sleek design with three variants.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Elderflame Frenzy', 'https://valorantstrike.com/wp-content/uploads/2020/07/Valorant-Elderflame-Collection-Frenzy-HD.jpg', 1600.40, '2020-07-10', 'The Elderflame Frenzy is part of the Elderflame Collection, known for its animated dragon design.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Forsaken Spectre', 'https://valorantstrike.com/wp-content/uploads/2021/04/Valorant-Foresaken-Collection-Spectre-HD.jpg', 1700.15, '2021-06-08', 'The Forsaken Spectre is part of the Forsaken Collection, with a cursed green aura and mystical symbols.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Protocol 781-A Bulldog', 'https://static.wikia.nocookie.net/valorant/images/e/e2/Protocol_781-A_Bulldog.png/revision/latest?cb=20230711202937', 2150.00, '2021-12-09', 'The Protocol 781-A Bulldog is part of the Protocol 781-A Collection, a high-tech futuristic weapon with custom audio.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Singularity Phantom', 'https://valorantstrike.com/wp-content/uploads/2020/10/Valorant-Singularity-Collection-Phantom-HD.jpg', 2150.75, '2020-10-13', 'The Singularity Phantom is part of the Singularity Collection, featuring a black hole aesthetic with custom animations.');

INSERT INTO valskins (Name, picture, cost, release_date, description)
VALUES ('Titanmail Bucky', 'https://valorantstrike.com/wp-content/uploads/Valorant-Titanmail-Collection-Bucky-HD.jpg', 1450.80, '2021-02-17', 'The Valorant Titanmail Bucky is part of the Titanmail Collection, a five skin bundle released on 11th May 2022. The full bundle includes a mace melee weapon, Frenzy pistol, Bucky, Vandal and Ares. The skins have a medieval theme, seen in the mace melee weapon as well as classic plain metal, armor style gun coatings');
