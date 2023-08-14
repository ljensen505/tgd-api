import sqlite3
from datetime import datetime
from models.db import DB


def populate():
    # Create a new database
    conn = sqlite3.connect(DB)

    # Drop tables if they exist
    conn.execute("DROP TABLE IF EXISTS Musicians")
    conn.execute("DROP TABLE IF EXISTS GroupTable")
    conn.execute("DROP TABLE IF EXISTS Events")
    conn.execute("DROP TABLE IF EXISTS Users")
    conn.execute("DROP TABLE IF EXISTS CarouselImages")
    conn.execute("DROP TABLE IF EXISTS Headshots")

    # Create the Headshots table
    conn.execute(
        """CREATE TABLE Headshots
            (id STRING PRIMARY KEY,
            url TEXT NOT NULL,
            musician_id INTEGER NOT NULL);"""
    )

    headshots = [
        {
            "id": "coco_hffqy5",
            "m_id": 1,
            "url": "https://res.cloudinary.com/dreftv0ue/image/upload/v1687022283/tgd-headshots/coco_hffqy5.jpg",
        },
        {
            "id": "margarite_ezzcsw",
            "m_id": 2,
            "url": "https://res.cloudinary.com/dreftv0ue/image/upload/v1687022284/tgd-headshots/margarite_ezzcsw.jpg",
        },
    ]
    for headshot in headshots:
        conn.execute(
            "INSERT INTO Headshots (id, url, musician_id) VALUES (?,?,?)",
            (headshot.get("id"), headshot.get("url"), headshot.get("m_id")),
        )

    # Create the CarouselImages table
    conn.execute(
        """CREATE TABLE CarouselImages
                (id STRING PRIMARY KEY,
                url STRING NOT NULL);"""
    )

    # Insert some sample data into the CarouselImages table
    img_urls = [
        {
            "id": "livingroom_bz0pp6",
            "url": "https://res.cloudinary.com/dreftv0ue/image/upload/v1687028716/tgd-carousel/livingroom_bz0pp6.jpg",
        },
        {
            "id": "wLTu18p_byqaov",
            "url": "https://res.cloudinary.com/dreftv0ue/image/upload/v1687028716/tgd-carousel/wLTu18p_byqaov.jpg",
        },
        {
            "id": "MandCthumbnail_image0-DELedit_copy_jdtngw",
            "url": "https://res.cloudinary.com/dreftv0ue/image/upload/v1687028712/tgd-carousel/MandCthumbnail_image0-DELedit_copy_jdtngw.jpg",
        },
        {
            "id": "studio_esvm3n",
            "url": "https://res.cloudinary.com/dreftv0ue/image/upload/v1687028710/tgd-carousel/studio_esvm3n.jpg",
        },
    ]
    for img in img_urls:
        conn.execute(
            "INSERT INTO CarouselImages (id, url) VALUES (?,?)",
            (img.get("id"), img.get("url")),
        )

    # Create the Users table
    conn.execute(
        """CREATE TABLE Users
                (id TEXT PRIMARY KEY UNIQUE,
                name TEXT NOT NULL);"""
    )

    # Insert some sample data into the Users table
    users = [
        {"name": "Lucas Jensen", "id": "google-oauth2|103593642272149633528"},
        {"name": "Margarite Waddell", "id": "google-oauth2|109109812131608294748"},
        {"name": "Coco Bender", "id": "google-oauth2|110044702811943457315"},
        {"name": "The Grapefruits", "id": "google-oauth2|116470512398914344676"},
        {"name": "Automation Tests", "id": "WQrIbh4gPU7ypcMKxxQA18eBGCOGfNxH@clients"},
    ]
    for user in users:
        conn.execute(
            "INSERT INTO Users (id, name) VALUES (?, ?)",
            (
                user.get("id"),
                user.get("name"),
            ),
        )

    # Create the Musicians table
    conn.execute(
        """CREATE TABLE Musicians
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT NOT NULL,
            headshot_id STRING,  -- Store the ID of the active headshot
            FOREIGN KEY (headshot_id) REFERENCES Headshots(id));"""
    )

    # Insert some sample data into the Musicians table
    conn.execute(
        "INSERT INTO Musicians (name, bio, headshot_id) VALUES (?, ?, ?)",
        (
            "Coco Bender",
            "Coco Bender is a pianist residing in the Pacific Northwest. She recently performed with Cascadia Composers, recorded original film scores by Portland composer Christina Rusnak for the Pioneers: First Woman Filmmakers Project, and during the pandemic presented a series of outdoor recitals featuring music by H. Leslie Adams, William Grant Still, Bartok, and others. Coco is a founding member of the Eugene based horn and piano duo, The Grapefruits, as well as a co-artistic director and musical director of an all-women circus, Girl Circus. She has taken master classes with Inna Faliks, Tamara Stefanovich, and Dr. William Chapman Nyaho. Coco currently studies with Dr. Thomas Otten. In addition to performing regularly, she teaches a large studio of students in the Pacific Northwest, from Seattle WA to Eugene OR. Coco was the accompanist for Portland treble choir Aurora Chorus, during their 2021-2022, season under the conductorship of Kathleen Hollingsworth, Margaret Green, Betty Busch, and Joan Szymko.",
            headshots[0].get("id"),
        ),
    )
    conn.execute(
        "INSERT INTO Musicians (name, bio, headshot_id) VALUES (?, ?, ?)",
        (
            "Margarite Waddell",
            "French hornist Margarite Waddell holds positions with the Eugene Symphony, Sarasota Opera, Boise Philharmonic, Rogue Valley Symphony, and Newport Symphony. As a freelancer, Margarite has played with ensembles throughout the West Coast including the Oregon Symphony, Portland Opera, Santa Rosa Symphony, Marin Symphony, and Symphony San Jose. She has performed with popular artists such as The Who, Josh Groban, and Sarah Brightman. Margarite can be heard on Kamyar Mohajer’s album “Pictures of the Hidden” on Navona Records. She appeared as a soloist with the Silicon Valley Philharmonic in 2016. Margarite cares deeply about music education and has taught private lessons, sectionals, and masterclasses throughout the Bay Area, Southwestern Oregon, Eugene, and Corvallis since 2013. She also performed in the San Francisco Symphony's Adventures in Music program for the 2016-2017 season. Margarite received her bachelor’s degree from the University of Oregon, and her master’s degree from the San Francisco Conservatory of Music.",
            headshots[1].get("id"),
        ),
    )

    # Create the Group table
    conn.execute(
        """CREATE TABLE GroupTable
                (name TEXT PRIMARY KEY UNIQUE,
                bio TEXT NOT NULL);"""
    )

    # Insert some data into the Group table
    conn.execute(
        "INSERT INTO GroupTable (name, bio) VALUES (?, ?)",
        (
            "The Grapefruits Duo",
            "The Grapefruits, comprising of Coco Bender, piano, and Margarite Waddell, french horn, are a contemporary classical music duo. They perform frequently through out the PNW with the goal presenting traditional classical french horn repertoire, new 20th century works, and commissioned works by PNW composers. Our upcoming concert series features works by Jane Vignery, Tara Islas, Gliere, Prokofiev, and Oregon Composers Christina Rusnak and Mark Jacobs.",
        ),
    )

    # Create the Events table
    conn.execute(
        """CREATE TABLE Events
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date DATETIME NOT NULL,
                description TEXT NOT NULL,
                image_url TEXT NOT NULL,
                location TEXT,
                ticket_url TEXT);"""
    )

    # Insert sample data into Events
    events = [
        {
            "name": "Summer Concert Series Eugene",
            "date": datetime(2023, 6, 6, 19, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "description": "Come hear The Grapefruits, Coco Bender and Margarite Waddell, perform horn and piano music. This fresh and joyous concert will feature works by Jane Vignery, Sergei Prokofiev, Reinhold Gliere, Tara Islas, and Southern Oregon composer Mark Jacobs.",
            "image_url": "Fairhill County and the Music Collaborative of Salguerro.png",
            "location": "First Church of Christ, Scientist\n1390 Pearl Street\nEugene, Oregon 97401",
            "ticket_url": "https://ticketstripe.com/eugenejune2023",
        },
        {
            "name": "Summer Concert Series Medford",
            "date": datetime(2023, 6, 2, 19, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "description": "Limited seating available and the start time is approximate. Please contact us directly to reserve a seat.",
            "image_url": "Fairhill County and the Music Collaborative of Salguerro.png",
            "location": "Medford, Oregon",
            "ticket_url": "",
        },
        {
            "name": "Classical On Broadway Series",
            "date": datetime(2023, 6, 25, 15, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "description": "Paul Safar and Friends. Featuring The Grapefruits Duo and trombonist Chris Shuttleworth. Chamber music of Amy Beach, Florence Price, Paul Safar, Robert Schumann, Chris Shuttleworth and Dante Yenque.",
            "image_url": "jazz-station.jpg",
            "location": "The Jazz Station\n124 W Broadway\nEugene, Oregon 97401",
            "ticket_url": "https://thejazzstation.org/#!event-list",
        },
    ]

    for event in events:
        conn.execute(
            "INSERT INTO Events (name, date, description, image_url, location, ticket_url) VALUES (?, ?, ?, ?, ?, ?)",
            (
                event["name"],
                event["date"],
                event["description"],
                event["image_url"],
                event["location"],
                event["ticket_url"],
            ),
        )

    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    populate()
