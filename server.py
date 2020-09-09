# coding: utf-8
import re
import copy
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)


current_id = 31

venues = [

    {
        "name" : "Rockwood Music Hall",

        "id" : 1,

        "image" : "https://media.timeout.com/images/101206475/750/422/image.jpg",

        "description" : "This LES haunt started as a tiny, cramped storefront space and has expanded into a multistage downtown fixture. Rockwood books an endless parade of aspirants, some of whom (such Chris Thile, Gabriel Kahane) have gone on to become stars of the singer-songwriter and Americana realms.",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Boris Lemeshev",
                "review" : "Great place if you want to see local bands perform. The acoustics are incredible and the sound system they use is top notch. Always great programs, covers, musicians, and the price is very reasonable. In total 3 stages for one music hall. Always nice to bring your friends to see a good concert and have a good time, and they have an open bar too, which is a plus."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Russell Wustenberg",
                "review" : "We came here with a friend to see a local artist perform a set. The venue is cozy and ideal for small music events. The artist was high-quality, and she had worked with major artists and labels so we were getting a bargain for the cost of the event. We didn’t drink, but there were waiters running around serving directly to the clients at their tables. Overall it was a wonderful evening and I would go back anytime I’m in the village!"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Nathan Drapela",
                "review" : "I really want to like this place, but I have some frustrations. I went to in stage 2 to see two solo singer/songwriter folk singers, one of whom I was familiar with and the other I had never heard before. Both singers were amazing and am very glad there are venues for performers like these. However, I was less impressed with the venue itself. While very cozy, it seems to operate more as a bar, where there happens to be live music than a performance space where they serve alcohol. There's apparently a 2 drink minimum for sitting and 1 drink minimum for standing."
            },
        ]
    },
    {
        "name" : "Arlene's Grocery",

        "id" : 2,

        "image" : "https://images.radio.com/wnewfm/styles/delta__775x515/s3/GettyImages-2762253.jpg",

        "description" : "Up-&-coming acts are the focus of this rock music bar that's also home to live-band karaoke.",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Nigel Buck",
                "review" : "Great place for drinking with a well stocked bar and good happy hour. Bar staff were excellent, security too. Was asked for ID, first time in 40 years."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Karen Buck",
                "review" : "For my husband who likes hard cider this was a great bar. Friendly and nice staff. We went early think it would get really busy also the toilets are not great!"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Jewel Swanson",
                "review" : "Awesome staff, excellent prices for the area, wonderful atmosphere, and a great time for all. A great place for drinks with friends, or, for a small cover, a great place to see energetic and awesome music in a very cool environment. If you went 6 times a month you wouldn't be bored with it, and you'd probably still be wanting more. 10/10, 5 stars, the works"
            },
        ]
    },

    {
        "name" : "Silvana",

        "id" : 3,

        "image" : "https://cdn.vox-cdn.com/thumbor/SDSKS3KFFCzTytAnZfExporxdtM=/0x0:960x720/870x653/filters:focal(407x338:559x490):format(webp):no_upscale()/cdn.vox-cdn.com/uploads/chorus_image/image/62579669/silvana.0.0.jpg",

        "description" : "Silvana in South Harlem is a testament to the truly unlikely things to be found in New York. It’s a Mediterranean restaurant and gift shop in one, serving superior casual eats like falafel and shawarma, while the downstairs room serves as both speakeasy and charmingly compact venue for world music.",

        "rating" : 4.4,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Kelsey Brow",
                "review" : "Enjoyed the food, music, service and reasonable prices. They need to turn down the volume of the music which was deafening at times."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Maddy Tervet",
                "review" : "Great atmosphere, High quality food and amazing pita and hummus. Definitely will be going back here. Great value for awesome middle eastern food and nice music too."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Brian Mayers",
                "review" : "Nice place for live music and drinks at night 🌃 . I love this place the vegan options are great."
            },
        ]
    },
    {
        "name" : "Barclays Center",

        "id" : 4,

        "image" : "https://assets3.thrillist.com/v1/image/2812830/size/tl-horizontal_main.jpg",

        "description" : "Best venue for an actually enjoyable arena experience. Manhattan’s iconic Madison Square Garden may be NYC’s most famous arena, but Brooklyn’s Barclays Center is an upgrade. First opened in 2012, Barclay’s has a clean, modern aesthetic, and it was designed with an eye toward the future of entertainment, featuring featuring improved acoustics and seating that make even the nosebleed seats worth the price of admission. And unlike MSG, it’s a world away from Midtown, meaning the massive concert crowds don’t have to compete with droves of tourists. -- SB",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Gene Yu",
                "review" : "New stadium that has pretty much all of the expected amenities you would come to expect, though I did appreciate the fact that they had multiple carts that also sold alcohol to alleviate long lines. Lot of foot traffic right around the stadium due its placement being surrounded by shops and restaurants. I sat in the lower 200s section for a Nets game and still found them to be really good seats to watch the game."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Melissa Caldero",
                "review" : "Can't go wrong at Barclays! Nice big space hosting a variety of events. My son had his college graduation here. There were 14,000 in attendance! Sound quality was really nice. As for food and drinks, as usual, as in any stadium, pricey but good."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Alex",
                "review" : "Awesome venue for a basketball game! Love the grey and black color scheme and the bright lights and architecture of the arena. A wide variety of food options and an entertaining in-game experience. The court looks very nice as well, especially with the new grey colors. The angling of the upper level provides a clear view of the action, even from the highest rows. Overall, a clean, modern arena that felt like a lounge from the moment I walked inside. Convenient subway exit right in front of the arena too. My primary critique would be the incredibly small distance between rows of seats on the upper level, it was difficult to maneuver even with people standing out of the way. I understand the need to hold more people, but a little more room would be nice. Otherwise, I definitely look forward to returning to Barclays Center in the future for another basketball game, maybe even making it a yearly tradition."
            },
        ]
    },
    {
        "name" : "Skinny Dennis",

        "id" : 5,

        "image" : "https://cdn.vox-cdn.com/thumbor/CTgHil9yVKcoWU79h0e6rLFM_PI=/0x0:4096x2613/870x653/filters:focal(1601x730:2255x1384):format(webp):no_upscale()/cdn.vox-cdn.com/uploads/chorus_image/image/62579685/IMG_1751.JPG.0.0.jpeg",

        "description" : "Even while Williamsburg rapidly evolves, Skinny Dennis always seems to stay the same, which is how the regulars like it. A holdover from the neighborhood’s punkier days, the unassuming honky tonk bar offers stiff drinks at the right price and is an energetic scene for country acts.",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Inspire Vetures, LLC",
                "review" : "Dive bar with a wide choice of beer and liquor specials for a great price. I was able to come here on a Saturday when they were having a live band. Definitely will come back!!"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Chris Pennells",
                "review" : "Incredible dive bar. Great selection of beers, awesome music, very friendly staff."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Jonathan Ritter",
                "review" : "This place is THE BEST. Rockin' Live Music, Great Hip Crowd, Friendly Bartenders. Packed and loud on peak nights, def the place to be! 10/10. As a brooklynite, this is one of local FAVES."
            },
        ]
    },
    {
        "name" : "The Apollo Theater",

        "id" : 6,

        "image" : "https://assets3.thrillist.com/v1/image/2813015/size/tl-horizontal_main.jpg",

        "description" : "Nothing tops showtime at the legendary Apollo Theater for a traditional experience amid Old New York ambiance and ornate design. The neo-classical theater is a cathedral of African American cultural history that made or broke stars of yore. Ella Fitzgerald debuted here, James Brown recorded one of the greatest albums of all time here, and a young Jimi Hendrix won an amateur night contest here in 1964. Greatness permeates the landmark building. Plus, a show at the Apollo is an excellent occasion to take advantage of Harlem’s excellent restaurant scene, including soul food classics like Amy Ruth’s and Sylvia’s and newer spots like Clay, ROKC, and Marcus Samuelsson’s Red Rooster. -- AG",

        "rating" : 4.6,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Elvin Rodriguez",
                "review" : "Went to Apollo.to buy my mother and aunt some jazz tickets. My mother loves Apollo and Red lobsters next door. It's a landmark. Lots of history walked through those doors. Comedy nights is the best for me but mommy loves jazz"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Allen Fields",
                "review" : "Amazing venue!  The Apollo Theater is a must visit concert site for any music fan.  Opeth was incredible, and the sound mix was stellar.  A treasure in the heart of Harlem.  I felt safe, welcome, and the staff went out of their way to accommodate my mobility issues.  Hats off to them!"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "bernard Greene",
                "review" : "First of all, I have been going to the Apollo Theater since I was a kid.I have seen a variety of singers & musicians over the years and have never been disappointed.This Holiday Gospel Celebration with Donald Lawrence & Yolanda Adams was no exception. The music was very inspirational, enjoyable and caused you to get involved in some way, whether singing along, patting your feet, clapping your hands, dancing in or out of your seat and even.....SHOUTING!"
            },
        ]
    },
    {
        "name" : "Lehman Center for the Performing Arts",

        "id" : 7,

        "image" : "https://assets3.thrillist.com/v1/image/2812947/size/tl-horizontal_main.jpg",

        "description" : "Lincoln Center might seem the obvious choice here, but the not-for-profit Lehman Center gets credit for bringing the fine arts beyond Manhattan. With venues like the Paradise Theater and the Olympic Theater Concert Hall shutting down over the years, the Bronx has had bad luck holding onto large performance spaces. But year after year, the 2,278-seat Lehman Center brings acts like Janelle Monáe, ballet performances, world dance and Salsa groups, and tributes to David Bowie to its stage. -- AG",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Ihor Strutynsky",
                "review" : "Good value for Your hard earned dollar. Clean. Comfortable seats. Clean bathrooms. Appropriate temperature. Good selection of talented, varied, national and international artists and company's. Easily accessible via Mass Transit. Problems resolved relatively well. Recommended."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Nancy J",
                "review" : "Concerts are awesome Doesn't matter where you sit all good . Reasonable  ticket prices."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Arleen Castillo",
                "review" : "Went to see Elvis Crespo in concert and it was amazing. The Lehman Center was spacious, clean and the staff who were working were top notch 👍 They had a lot for parking and the $10 was worth not looking for a spot and it was close to the entrance of the campus. Overall a great experience and can't wait for the next concert there"
            },
        ]
    },
    {
        "name" : "Birdland",

        "id" : 8,

        "image" : "https://cdn.vox-cdn.com/thumbor/I_6-cv0OI6ktuSJgVEVlVvz5pIc=/0x0:2048x1173/870x653/filters:focal(763x436:1089x762):format(webp):no_upscale()/cdn.vox-cdn.com/uploads/chorus_image/image/62579670/17_og.0.0.jpg",

        "description" : "Birdland in the Theater District, started in 1949, is a reprieve from its Midtown surroundings with a romantic, red-lit bar that books top-notch acts — including jazz icon Freddy Cole, Brazil-born Eliane Elias, and the virtuoso house band — and serves Cajun-influenced dishes worth seeking out. With a $10 food/drink minimum per person, food isn’t necessary, but the crab cake with cherry tomatoes and remoulade or jambalaya loaded with crawfish, chicken, sausage, and bacon are both worth ordering. Tickets are available in advance or at the door.",

        "rating" : 4.7,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Philip Vassallo",
                "review" : "The jazz capital of the world! Great music, excellent sight lines, tasty food, friendly service."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Tony Pham",
                "review" : "Went to Jim Caruso's cast party on Mondays and it was a good time. Lots of first time and repeat performers with a variety of musical talent. Also tons of regulars in the crowd who bring energy to the room. Jim was telling us how Martin Short dropped by one evening and did standup, but that might be a rare occasion. My favourite part of the show have to be how the pianist, bassist, and drummer picked up songs so quickly.  Also don't sit/stand on the piano if you are performing."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Chris Welty",
                "review" : "Birdland was not founded by Charlie Parker, and this is not the original nor the second location, but I'm sure it's a prime spot for tourists.  Lots of big names come here, you've got the cast party on Mondays which is a lot of fun. Big cover charge (30-50) and a $10 minimum makes this an expensive offering for jazz, there are a lot of good places for much less. But if you want the biggest names, it's here, blue note, or Vanguard... and of the three, birdland is the best. Why? They treat you like a human being. Nice staff, nice space with a bit of elbow room, great sounds. Dizzys club is a bit nicer but hasn't quite risen to the level of getting the top names nor does it have the history. Birdland is the best jazz club in NY, making it the best in the world."
            },
        ]
    },
        {
        "name" : "H0L0",

        "id" : 9,

        "image" : "https://lh5.googleusercontent.com/p/AF1QipOwJW8lO7vlrHcMaV2cVKCtTcEhPYCzYfPbB9JS=w408-h306-k-no",

        "description" : "H0L0’s entrance is almost as obscure as its minimal online presence, giving your stop here a twinge of hush-hush cool. Inside, the industrial, intimate, gallery-like space is equally fit for DJs, pop acts, and rappers. Technicolor lights and visuals further the artsy air. Here, you’ll get up close and personal with emerging artists and you’re likely to catch the next underground great. -- SB",

        "rating" : 4.3,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Jamekia Swepson",
                "review" : "Great place for new artists to try music. Crowd is eclectic"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "DJ Transaction",
                "review" : "I give extra star because I played there and I like it personally. The problem with this place is that it's in the middle of no where and I can't see anyone going here unless there is a big promoted event."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Thiago DeMoura",
                "review" : "The team at dub day has made a place where progressive thoughts and sounds could be accepted. HOLO was the space in which that idea was able to come alive and we thank the staff and venue for letting us use it on a weekely basis."
            },
        ]
    },
        {
        "name" : "Rough Trade",

        "id" : 10,

        "image" : "https://assets3.thrillist.com/v1/image/2813012/size/tl-horizontal_main.jpg",

        "description" : "Originally a British music label and chain of record stores, the sole Rough Trade on this side of the Atlantic features the same vibe as London’s Rough Trade East: a duel record store/music venue combo. The back performance area is tiny, but its retail adjacency has its perks. In addition to concerts, artists also often sign records before or after shows, there a few free, acoustic sets on weekend afternoons, and fans can score invites to exclusive listening parties ahead of album releases. -- SB",

        "rating" : 4.7,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "warren huberman",
                "review" : "For those of you who can remember, this is as close to Tower and Virgin that you can get in 2020. Great selection, nicely laid out and with several listening stations (!) for the latest releases. Prices are fair as well. Mostly for new releases but there is some used stuff too. Worth the trip!"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "John J",
                "review" : "Amazing store. I could spend all day in here. Great selection, carefully curated displays. Large and welcoming. Very good vibes"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Brian Ferdman",
                "review" : "Half record store and half performance space, Rough Trade was built from old ship containers, giving it a cool vibe (which can also lead to some cool drafts in winter). The record store is spacious, and the performance venue is excellent, affording patrons with very good sound and mostly good sight lines. While the balcony railing can occasionally get in the line of sight for those patrons, the balcony itself is fairly spacious and offers limited bench seating. A downstairs bar keeps customers sated."
            },
        ]
    },
        {
        "name" : "The Flatiron Room",

        "id" : 11,

        "image" : "https://cdn.vox-cdn.com/thumbor/UlKZ7e3RckoGErIB_sskuco8Sis=/0x0:3000x2000/870x653/filters:focal(1260x760:1740x1240):format(webp):no_upscale()/cdn.vox-cdn.com/uploads/chorus_image/image/62579672/_DSC0212.19.jpg",

        "description" : "The Flatiron Room is a haven for those in Flatiron looking for a great cocktail in a sophisticated bar, sans all the attitude. Booze aficionados will love the whiskey-centric bottle list, which includes the option to buy a favorite and keep it behind the bar, while small bites and a rotating schedule of live music make it worth hanging out in all night.",

        "rating" : 4.6,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Katie Angelova",
                "review" : "Classy place, cozy atmosphere, good live jazz, great food, stellar drink menu. Definitely one of my favorite places to celebrate!"
                },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Evan Tsun",
                "review" : "Great place to have a classy drink. Live Music every night, fantastic whiskey selection, very knowledgable staff. Can't lose. It also never gets too crowded because they only let people in if there are seats or spots at the bar."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "J Gudger",
                "review" : "Absolutely terrific music & ambience, unbeatable bourbon whiskey selection. Good food menu and reasonable value for the area."
            },
        ]
    },
        {
        "name" : "LunÀtico",

        "id" : 12,

        "image" : "https://assets3.thrillist.com/v1/image/2812832/size/tl-horizontal_main.jpg",

        "description" : "Many NYC music venues are attached to a bar, but here we mean a place where the music and the bartending happen in same space. There is no better spot than Bar LunÀtico. The Bed-Stuy restaurant and bar sports a live act every single night from an impressive range of global, jazz, blues, and rock acts -- Daptone soul singer Naomi Shelton regularly performs at the Sunday gospel brunch. The hyper-intimate space, mostly occupied by small café tables, and first-come-first-served policy makes for a truly unique neighborhood vibe. Coming for a drink, meal or coffee is like listening to music at a friend’s house. -- AG",

        "rating" : 4.7,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Karen Glenn",
                "review" : "Went to the Sunday Gospel brunch - what an experience! Beverly Crosby on vocals and Greg Monk on the organ. Such an emotional and beautiful performance. Beverly has  a powerful and moving voice in such an intimate setting-really something special. Loved the bar staff and cocktails- this place has a real appreciation for musicians. Would highly recommend- and will definitely be coming back"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Brad Klein",
                "review" : "Solid neighborhood bar. Packed when there's funky live music in the back. Menu looks delicious - will be back!"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Dan Calladine",
                "review" : "A great local bar.  We went for the weekend brunch (inc live music on a Sunday) and could not have had a better time.  Great food, excellent iced coffee, and a wonderful vibe"
            },
        ]
    },
        {
        "name" : "The Bitter End",

        "id" : 13,

        "image" : "https://lh5.googleusercontent.com/p/AF1QipMMQp_hGADGyjgbmampZIhmKNM_lRqiU1aRezRO=w408-h306-k-no",

        "description" : "The Bitter End is a 230-person capacity nightclub, coffeehouse and folk music venue in New York City's Greenwich Village. It opened in 1961 at 147 Bleecker Street under the auspices of owner Fred Weintraub. The club changed its name to The Other End in June 1975. However, after a few years the owners changed the club's name back to the more recognizable The Bitter End. It remains open under new ownership.",

        "rating" : 4.3,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "J Droid Dennis",
                "review" : "Great music every night! The service is exceptional, especially Ann our waitress. Checks drinks if empty, but not intrusive. Remembered all drinks and prompt service. (Tip generously!) This place has introduced some greats and still has unique and talented acts to this day. Can anyone say Robert Zimmerman?"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Rick Culleton",
                "review" : "Good music and a good time. Twice I've seen great cover bands here. Last night they closed with a very good Zeppelin song. Well worth the $10 cover. There are a handful of live music venues on Bleaker and a couple good places to eat. This part of town makes for a great night out."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Sarah Lee",
                "review" : "Wow, such a cool bar! I highly recommend this place if you enjoy live music, drinking, and love to meet weird people. Great staff and super hip interior. It's a small bar, but it's definitely a great place to listen to amazing music and just have a great time. Also keep in mind that you will have to order 2 drinks per band/show that performs."
            },
        ]
    },
        {
        "name" : "Forest Hills Stadium",

        "id" : 14,

        "image" : "https://media.timeout.com/images/102626829/380/285/image.jpg",

        "description" : "After extensive renovation, this storied tennis stadium—home to memorable matches and concerts from the ’20s through the ’80s (including the Beatles, Stones and others)—reopened its doors in 2013 with a rowdy Mumford & Sons gig. These days, the venue regularly hosts a wide variety of artists ranging from Chainsmokers to Van Morrison.",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Seth Ayers",
                "review" : "Forest Hills Stadium is one of the nicest music venues I've been to.  It's got a tiny music festival vibe to it;  Great drinks, plenty of options for food, and almost no lines for the restrooms.  The show itself was wonderful, great acoustics."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Arthur Shatz",
                "review" : "Great venue. Easy to get to by public transit. Superb sound system.  Beautiful clean brand new restrooms. Outstanding and varied food court. Bleacher seats have no seat backs, but not a big deal unless you have back problems."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Julissa Herrera",
                "review" : "Public transportation commute to the stadium was not complicated. The security line was smooth and quick. Staff was incredibly friendly. And space itself provided great seating options and view. I didn't used restroom or buy any food or drinks but there seems to be plenty of those. Be sure to dress accordingly as it's outdoor and can get breezy and cool up on the top tiers. Enjoy the experience I'd highly recommend."
            },
        ]
    },
    {
        "name": "Bowery Ballroom",

        "id": 15,

        "image": "https://assets3.thrillist.com/v1/image/2812852/size/tl-horizontal_main.jpg",

        "description": "A decently sized bar and lounge downstairs and stairs at both the front and the back of the 575-person capacity performance space help keep crowd movement fluid -- or the place’s knack for catching acts just as they are beginning to have their moment, there’s a special alchemy that makes a show at the Bowery great. It also doesn’t hurt that Bowery Ballroom is smack in the middle of the food and drink hub of the Lower East Side, providing fantastic options for pre- and post- show fun.",

        "rating": 4.6,

        "current_review_id" : 4,

        "reviews": [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user":"Penny Pennell",
                "review": "when we discovered our favourite band was touring and playing at the Bowery we decided it would be a perfect reason to go to NYC for the weekend.  As a Canadian, I've heard of this venue over the years and thought it would be great to check out. It did not disappoint. We stood at the back bar and had fantastic sight lines. The hype is real! This is a fantastic live music venue."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user": "Carol Campion",
                "review": "Saw Shannon Lay who performed with Ty Seagull and I was blown away! The show was very well liked by everyone in the balcony and on the floor. It was fantastic. I met people who traveled from Canada 🇨🇦 just to see Shannon . Ty’s wife also gave me a CD . Thanks Great Place/ Show/ People who work here are All fabulous!!!"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user":"Candypie 2010",
                "review":"The place is nice and spacious for a good crowd of 568 people only wish the bar had better choices from drinks mostly all they have are beer drinks. my friend also said the sound system need to be a little better when they sing and be a little creative with the background settings other than that I enjoyed myself and the performance"
            }
        ]
    },
        {
        "name" : "Music Hall of Williamsburg",

        "id" : 16,

        "image" : "https://media.timeout.com/images/100108711/380/285/image.jpg",

        "description" : "Run by local promoter Bowery Presents, this Williamsburg outpost is basically a mirror image of similarly sized Bowery Ballroom, one upping its Manhattan counterpart with improved sightlights—including elevated areas on either side of the room—and a bit more breathing room. With booking that ranges from indie-rock bands to hip-hop acts, it's one of the best rooms in New York to see a show.",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Chris Meyer",
                "review" : "Venue has very good sound quality and a cool vibe. It took ages to get in due to security. Very happy to feels safe but wish there was a more streamlined system. I'd definitely see other shows here but would suggest you arrive early."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Leifur Björnsson",
                "review" : "Love this venue. Size is good and it always sounds nice. I've seen and played a number of shows here. The area around it is nice, walk a few steps to get a great view of Manhattan and the river, good restaurants and etc. The area has gotten gentrified a lot these past few years, used to be better, more authentic, but still it's a nice spot."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Harpy Monet",
                "review" : "Very efficient security and ticketing process! Had lots of fun. Very convenient bar and restroom downstairs of the main music hall. Awesome time!"
            },
        ]
    },
        {
        "name" : "Beacon Theatre",

        "id" : 17,

        "image" : "https://media.timeout.com/images/100262465/380/285/image.jpg",

        "description" : "This spacious former vaudeville theater, resplendent after a recent renovation, hosts a variety of popular acts, from Steely Dan to Ryan Adams. While the vastness can seem daunting for performers and audience members alike, the gaudy interior and uptown location make you feel as though you’re having a real night out on the town. ",

        "rating" : 4.7,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Paul faria",
                "review" : "Beautiful theater.  The seats are a little tight for wider guys like myself but I still found them comfortable.  They also had plenty of beverage stations on each floor to keep the lines short. We saw Seinfeld there and the acoustics were great. I would definitely recommend going just to see the interior.  It is a style that would be hard to replicate today."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Chris Becker",
                "review" : "Love this venue. The architecture is historic. The bar and bathroom lines are long but what's new. Definitely a great place to see a show whether you're on the floor or the balcony"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "C P",
                "review" : "First time going there located in the Upper Westside. Absolutely love the elegant, classy exterior. Very tastefully decorated, three tiered theatre, seats over 2000, the stage is well designed you can get a great view wherever you are sitting."
            },
        ]
    },
        {
        "name" : "The Iridium",

        "id" : 18,

        "image" : "https://media.timeout.com/images/105486614/380/285/image.jpg",

        "description" : "Live music seven days a week? We'll take it. The Iridium, a musical landmark centered in the heart of Times Square, has been serving New York City concert...",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Bogdan Iordachita",
                "review" : "Excellent experience. Very nice place to disconnect from all the rush outside and enter the wonderful world of jazz. Very good service even if the place was crowded."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "c g",
                "review" : "Great place. Amazing food. Amazing night of Sharon Klein Productions particularly Boys of the Bandstand. They were absolutely amazing had the whole house rocking hope that they are permanent member of the iridium.  Great time"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "THE GOLDEN PIE .",
                "review" : "Event itself was amazing and I will admit it’s a lovely little venue. But I have literally never and I mean never had such an appalling experience when it came to a simple overcharge on my card. Don’t bother trying to call them. Won’t happen. Maybe an email to say? Doesn’t work. As for the way the Facebook page acts it’s both shocking and laughable. 55 dollars down and I get offered t shirts. That most likely cost very very little. The other offer was 2 tickets to a show which I admit is admirable and were I still there I would have taken them up on the offer. "
            },
        ]
    },
        {
        "name" : "Radio City Music Hall",

        "id" : 19,

        "image" : "https://media.timeout.com/images/100559627/380/285/image.jpg",

        "description" : "One heralded as the Showplace of the World, this famed Rockefeller Center venue has razzle-dazzled patrons since the 1930s with its elaborate Art Deco details, massive stage and theatrics. Though best known as the home of the Christmas Spectacular, which stars the high-kicking Rockettes and a full cast of nativity animals, many musicians consider the 6,000-seat theater a dream stage to perform on, including a recent extended stay from Lady Gaga and Tony Bennett.",

        "rating" : 4.7,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Zebby Clark",
                "review" : "I went around Christmas time for my girlfriends birthday. We had a wonderful time and the winter spectacular was amazing. We had such a great time. The staff was very friendly and helpful. I’ve to a lot of shows in New York radio city has the best staff. Get any seat, they all have wonderful views of the stage. Definitely will be back!"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "K. West",
                "review" : "I had great seats for the Jill Scott concert. But what was most amazing about this experience was the effective handling of long line to the women's bathroom. It went by quickly because an employee directed people to a stall when it became available. I know it seems crazy for that to stand out but for such a crowded facility this was an amazing experience."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Amber Evans",
                "review" : "Radio City Music Hall is absolutely breathtaking, especially during Christmas time! We've taken the tour before which was a really amazing experience. The coolest part of that was being in the light/ sound area and looking down on the performance on stage. The year after, we got the pleasure of seeing The Christmas Spectacular with the Rockettes. Not only were the dancers phenomenal, but the entire show was mesmerizing to watch. They even had live animals (camels, a sheep, and a donkey) which was so cool to see! I had no idea going into it. Highly recommend this show, it was absolutely amazing!"
            },
        ]
    },
        {
        "name" : "Saint Vitus",

        "id" : 20,

        "image" : "https://media.timeout.com/images/100316543/380/285/image.jpg",

        "description" : "This Greenpoint club—moodily decorated with all-black walls and dead roses hanging above the bar—is one of the best places in the city to see metal, rock and more experimental heavy music, with reliably loud bands typically booked seven nights a week.",

        "rating" : 4.7,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Monica Hernandes",
                "review" : "Amazing times at Saint Vitus. Awesome bartenders and friendly crowd. Great place to chill and have a few drinks. Alcohol prices are good. When Big name bands play at the venue it can get extremely packed, but overall bar is a great place."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Alejandro4891 .",
                "review" : "I've been going to metal shows since 2008 and this bar since 2012. Throughout the years and various venues I've been to, this is without a doubt one of or my absolute favorite venue for metal shows. "
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Steve M.",
                "review" : "the first time that I was trying to looking for this bar was very tough but the second that you know where it is you always want to come back to it. The interior in the bar itself was out-of-this-world I've never seen before. I went here for a small rock concert that they were holding and it was really awesome time listen to the bands at their venue. "
            },
        ]
    },
        {
        "name" : "Village Vanguard",

        "id" : 21,

        "image" : "https://media.timeout.com/images/100206113/380/285/image.jpg",

        "description" : "After more than 80 years, this basement club’s stage still hosts the crème de la crème of mainstream jazz talent. Plenty of history has been made here—John Coltrane, Miles Davis and Bill Evans have grooved in this hallowed hall—and the 16-piece Vanguard Jazz Orchestra has been the Monday-night regular since 1966. Thanks to the venue's strict no cell phone policy, seeing a show here feels like stepping back and time. It's just you and the music. ",

        "rating" : 4.7,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Ritesh Poddar",
                "review" : "The vanguard's music set was exquisite. The 16 piece jazz group had everything. It is a cosy place and if you want the best seats, it is best to arrive early. We reached at 10 pm for a 10:30 pm show and all we got was seats at the back. We probably should have arrived 45 minutes before to get better seats but the jazz was great."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Agata Petromilli",
                "review" : "Cool drinks, cool vibe. If you're a jazz lover, you gotta come here and give this place a chance. You'll also find great artists and performers."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Scott Sperling",
                "review" : "One of the world's great jazz clubs. Literally, a hole in the wall. Actually, literally a hole in the ground, but that doesn't matter: great atmosphere, great music, always full to the gills. Get there early to get a seat with decent sight lines."
            },
        ]
    },
            {
        "name" : "Blue Note",

        "id" : 22,

        "image" : "https://media.timeout.com/images/100433851/380/285/image.jpg",

        "description" : "The Blue Note prides itself on being the jazz capital of the world. Bona fide musical titans (Chick Corea, Ron Carter) rub against hot young talents, while the close-set tables in the club get patrons rubbing up against each other. Arrive early to secure a good spot—and we recommend shelling out for a table seat.",

        "rating" : 4.4,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Scott Sperling",
                "review" : "One of the great jazz clubs. What more can I say? Get here early to get a good seat. Warning: you are packed in! You'll get to know your neighbor well. Thus, the importance of getting here early: in order to get an end seat. As for the music, well you already know it's the best..."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Sol ,",
                "review" : "Great venue, but you might wanna avoid sitting nearby the piano as the seats are very close to the bar. It gets a bit noisy at the start even though all the employees are very nice and trying hard not to make unnecessary noises. But Blue Note is one of my favourite jazz venue for sure!"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Sagy Langer",
                "review" : "Went to see the Dizzy Gillespie All Stars. Really enjoyed it. Sound was good, atmosphere is cozy and food was okay. Even though it was an \"All star\" show, it was very enjoyable. Every performer on stage was really gifted, and the pianist is a prodigy! He \"stole\" the show."
            },
        ]
    },
            {
        "name" : "Kings Theatre",

        "id" : 23,

        "image" : "https://media.timeout.com/images/101898503/380/285/image.jpg",

        "description" : "Once one of Brooklyn’s most elegant movie theaters, the Loew’s Kings Theatre opened in Flatbush as a movie and live performance space in 1929. When multiplex cinemas became popular in the 1950s, the theater lost traction with audiences. It eventually closed in 1977 and the stunning interior fell into disrepair. After an elaborate $95 million restoration, the 3,074-seat theater reopened in 2015 in all its original glory. Catch classic acts and rising stars alike at the ornate theater.",

        "rating" : 4.6,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Brian Kaplan",
                "review" : "I'm old enough that I choose concerts based on the quality of the venue and I love Kings Theatre. The acoustics and sound system alone should make you want to see shows here but the quantity, variety and distribution of bars, the friendly staff, and all housed in a gorgeously renovated historic theater make it a superb venue. Only drawback is the less than ideal restroom situation but that only dings the score one star."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Heather Owen",
                "review" : "Seating was comfortable and not cramped, but the way they allowed ticketholders in leaves something to be desired. We showed up before doors opened and walked for several blocks to reach the end of the entry line. By the time we entered the venue doors, the show had been going on for 20 minutes already. Also, one of the employees asked my partner why they were using a cane. That seemed a little insensitive."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Everlina - Whynter Thomas",
                "review" : "The Hiphop Nutcracker was simply AMAZING. The cast outdid themselves. Mr. Curtis Blow was an awesome host who had the crowd going. Can't wait to see what else they have in store for future performances."
            },
        ]
    },
            {
        "name" : "Mona's",

        "id" : 24,

        "image" : "https://cdn.vox-cdn.com/thumbor/oJI-3ifpIlvtkyu4y0Lj92fcCU8=/0x0:960x494/870x653/filters:focal(419x105:571x257):format(webp):no_upscale()/cdn.vox-cdn.com/uploads/chorus_image/image/62579677/24177003_1510228115699713_7598837388549308572_n.0.0.jpg",

        "description" : "Mona’s is the answer to New Yorkers wondering where they can still find a bit of the old East Village. Divey to the point of being bunker-like, it nevertheless keeps the crowd smiling with cheap beer, pleasant bartenders, and a rotating schedule of live music that includes a raucous Tuesday jazz night.",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Charlson Ho",

                "review" : "Amazing service and drinks are very tasty.  The environment is very chill."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Schotty Leach",
                "review" : "This is the place!  I come here on Tuesdays for the jazz jam.  Best event ever.  Casual environment and high level jazz music all night."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Guadalupe Astorga",
                "review" : "Good ambience, nice gigs, although it’s a bit small"
                },
        ]
    },
            {
        "name" : "Le Poisson Rouge",

        "id" : 25,

        "image" : "https://media.timeout.com/images/100202089/380/285/image.jpg",

        "description" : "Situated in the basement of the long-gone Village Gate—a legendary performance space that hosted everyone from Miles Davis to Jimi Hendrix—Le Poisson Rouge was opened in 2008 by a group of young music enthusiasts with ties to both the classical and indie-rock worlds. With a top-notch sound system and modular stage that can be set up for in-the-round performances, LPR sounds great whatever the genre is.",

        "rating" : 4.4,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "William Polito",
                "review" : "Awesome place to see a band. Felt comfortable in the space provided. Not too big not too small. Great cornered stage layout. Staff was inviting. Drinks a bit pricey but I'm sure their rent is too. Great location."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "ZayP The IAm",
                "review" : "It's a decent sized dance floor.... And a lil side gallery for seating away from the crowd... Great party space... Open yet intimateWay overpriced drinks... Wasn't even giving straws... But besides that was cool🤷🏾‍♂"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Brian Ferdman",
                "review" : "The former home of the historic Village Gate Theater, where the likes of Bob Dylan and Janis Joplin once graced the stage, this subterranean venue generally features very good sound. Seated shows tend to suffer from the typical \"jazz seating\" arrangement, i.e. patrons are crammed into place and may have to contort their head in strange angles to see the stage. General Admission shows tend to be a nicer experience, although sold out shows can be jam-packed. The VIP section is tucked into a back corner on a platform. The bar offers a decent selection of cocktails and has solid food. Be forewarned that your phone will likely have minimal service this far underground."
            },
        ]
    },
            {
        "name" : "Pianos",

        "id" : 26,

        "image" : "https://media.timeout.com/images/100110597/750/422/image.jpg",

        "description" : "In recent years, a lot of the cooler bookings have moved from Pianos to Brooklyn or down the block to venues such as Cake Shop. Still, while sound is often lousy and the room can get uncomfortably mobbed, there are always good reasons to go back—very often the under-the-radar emerging rock bands that make local music scenes tick.",

        "rating" : 4.0,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Courtney Burstion",
                "review" : "Came through to see @Lambrabbit rock the 1s and 2s.... Phenomenal. She's knowledgeable and immensely talented with a diverse range of genres✨✨✨ But from what I gather this is a generally dope spot for music. Check it out, and bring your State Issued ID! They don't accept IDNYC"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Alberto",
                "review" : "This is the place to be! You party for cheap and actually have fun! It's super packed but the line to get in moves relatively fast. You will be dancing all night with a college crowd that's super diverse"
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Raymond R-Mcnaught",
                "review" : "Great place to play. Downstairs has a great PA for bands. Upstairs has decent sound. The Dj upstairs on Wednesday is fire. "
            },
        ]
    },
            {
        "name" : "The Town Hall",

        "id" : 27,

        "image" : "https://media.timeout.com/images/100292137/380/285/image.jpg",

        "description" : "Acoustics at the 1921 people’s auditorium are superb, and there’s no doubting the gravitas of the Town Hall’s surroundings. The building was originally designed by illustrious architects McKim, Mead & White as a meeting house for the League for Political Education, a suffragist organisation. George Benson, Grizzly Bear and Lindsey Buckingham have performed here in recent times, and smart indie songwriters such as the Magnetic Fields have set up shop for a number of nights.",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "shanikka white",
                "review" : "Nice intimate place. Seats space a bit small but manageable. The Mockingbird project was excellent very insightful and informative. I think everyone should watch this. I wish more of my coworkers attended due to dealing directly with mass incarceration."
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Erica Loberg",
                "review" : "I saw City and Colour here, and the acoustics in this venue where phenomenal. It’s the perfect sized theater to maintain an intimate feeling while also enabling the excited energy of a large enough crowd. It’s kind of an old building, which adds interesting character (since I didn’t experience any problems because of that)."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Adam Ford",
                "review" : "This is such a quintessential New York institution. The seats are comfortable in the view lines are all good. I love the historical information posted on the walls upstairs. I wish I could have been there for the Margaret Sanger riot in 1921."
            },
        ]
    },
            {
        "name" : "United Palace Theatre",

        "id" : 28,

        "image" : "https://media.timeout.com/images/101304621/380/285/image.jpg",

        "description" : "This renovated movie house, which was once a vaudeville theater, dates from the 1930s. It really does feel as if you’ve entered a palace here, with the shimmering chandeliers, ornate ceiling and gold-drenched corridors. Over the past few years, the venue’s bookings have ranged from popular young acts such as Adele, Vampire Weekend and Bon Iver to stalwarts of the music world like Bob Dylan and the Allman Brothers Band. Though it's located at the top end of Manhattan, far beyond the traditional nightlife or tourist zone, the theater is nevertheless easily accessible by subway.",

        "rating" : 4.5,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "U-roy Felix Agboli",
                "review" : "My church held a Sunday service is this magnificent edifice today and my experience was inexplicable. The place is ginormous and colorful with gold finish. The interior is an architectural marvel; the creativity, the layout, the distinctiveness is ethereal. This spellbinding theatre was built in 1930 with a seating capacity of 3,327. It’s pretty close to the road and can be easily noticed from a vehicle in normal traffic. There’s also wheelchair accessible for the differently able"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Sandra",
                "review" : "This is a beautiful large venue. It fits a little less than 3,400 people. The interior is stunning and awesome for some aesthetic Instagram photos. It is far up, but it is magical venue. My church was here for a field trip service and now meets here regularly every Sunday. Everyone loves the venue."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Michelle H",
                "review" : "This building is exquisite. It is majestic. There are 2 bars, one on each level."
            },
        ]
    },
            {
        "name" : "Carnegie Hall",

        "id" : 29,

        "image" : "https://media.timeout.com/images/100202927/380/285/image.jpg",

        "description" : "Since it first opened its doors in 1891, Carnegie Hall has been a mainstay of the New York music scene. George Gershwin, Louis Armstrong and the Beatles have all performed here, and to this day, artistic diector Clive Gillinson continues to put his stamp on the renowned concert hall. Whether you catch a show in the Isaac Stern Auditorium, Zankel Hall or the Weill Recital Hall, you're sure to be dazzled by the history and ambiance of the place.",

        "rating" : 4.7,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Jennifer Bondurant-Magnone",
                "review" : "I so enjoyed joining my cousin Rain Worthington for an orchestra performance featuring one of her composed pieces. It was a beautiful evening with my family and friends! So proud of Rain & how far her NYC journey has come! Carnegie hall is a wonderful experience!"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "George Gregoriou",
                "review" : "The legendary venue is a must see, whether you're in Manhattan for an evening or have been for a lifetime. If legroom is a priority, book seats on the Parquet or First Tier, as the rest of the levels (especially the second tier) are a \"cozy\" fit. As far as acoustics go, there isn't a single bad seat in the house."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "redwillow ",
                "review" : "Place was cool. I had a balcony seat and felt I could see the stage fairly well. Sound was a bit stained but that could just be my hearing. The elevator was not publicized very well and the walk up was an exercise but not the end of the world. Atmosphere wasn't stuffy - at least not in the balcony. A wonderful experience overall."
            },
        ]
    },
            {
        "name" : "Webster Hall",

        "id" : 30,

        "image" : "https://media.timeout.com/images/101216599/380/285/image.jpg",

        "description" : "Built in 1886, Webster Hall has been through several iterations (and names) before settling into its tenure as a high-caliber concert venue. In the 1950s, performers like Tito Puente and Woody Guthrie graced the stage, and when it was known as The Ritz in the '80s, the same venue hosted rock legends like U2, Eric Clapton and Guns N' Roses. These days, you can expect to find indie acts like Animal Collective and The Maine, as well as hip-hop artists like Wiz Khalifa and Mobb Deep. Just be sure to show up early if you want a decent view.",

        "rating" : 4.1,

        "current_review_id" : 4,

        "reviews" : [
            {
                "id" : 1,
                "mark_as_deleted" : False,
                "user" : "Courtneay Fitts",
                "review" : "I love Webster Hall!  Huge venue and the staff there are cool and laid back while still being very attentive. They have a nice lounge area near the entrance/exit where you can enjoy some drinks and snacks at the bar before heading upstairs to the main stage areas.  There are bars scattered everywhere throughout so you will never go thirsty ;)"
            },
            {
                "id" : 2,
                "mark_as_deleted" : False,
                "user" : "Megan Eiswerth",
                "review" : "Mixed feelings about this place. Pros: Large venue with freedom to roam the floor or the balcony. Lounge/ bar area downstairs by the bathrooms where you can still hear the music and watch from screens. Average beer prices. Good sound and light production. Security thoroughness is average. Good location, easy to get to.Cons: Excruciating lines. I have been stuck in entry lines that wrap around the block, even an hour+ after doors opened. THEN once inside, I had to wait almost 40 minutes to check my coat. It seems like their staff/ organization is just really sloppy. I've also had experiences where staff is very short-tempered and rude, either yelling or pushing past, unprovoked."
            },
            {
                "id" : 3,
                "mark_as_deleted" : False,
                "user" : "Sean Murray",
                "review" : "One of the best concert venues in New York because they truly customize the experience to each artist and bring in the best acts. The entire place is newly renovated and easy to navigate. I'm tall, so I don't mind the standing room only, but I have seen shorter people get annoyed when they have to jockey for space to see the stage. Will be going back soon!"
            },
        ]
    }
]

@app.route('/')
def search_page():
    search_result = []
    return render_template('home_page.html', venues=venues)

@app.route('/search/<search_string>')
def search(search_string=None):
    global venues

    search_result = []
    for i in venues:
        if search_string.lower() in i["name"].lower():
            search_result.append(copy.deepcopy(i))
        elif search_string.lower() in i["description"].lower():
            search_result.append(copy.deepcopy(i))

    for i in range(0, len(search_result)):

        desc = search_result[i]['description']
        desc = re.sub(search_string, r"<span class='highlight'>\g<0></span>", desc, flags=re.IGNORECASE)
        search_result[i]['description'] = desc

        name = search_result[i]['name']
        name = re.sub(search_string, r"<span class='highlight'>\g<0></span>", name, flags=re.IGNORECASE)
        search_result[i]['name'] = name


    return render_template('search_page.html', search_result = search_result, venues=venues)

@app.route('/view/<id>')
def view(id=None):
    global venues
    venue = {}

    for i in venues:
        if id == str(i["id"]):
            venue = i;

    return render_template('view_page.html', venues=venues, id=id, venue = venue)

@app.route('/create')
def create_page():
    return render_template('create_page.html', venues=venues)

@app.route('/save_venue', methods=['POST'])
def save_venue():
    global venues
    global current_id

    json_data = request.get_json()
    new_name = json_data["name"]
    new_image = json_data["image"]
    new_description = json_data["description"]
    new_rating = json_data["rating"]
    search_result=[]

    new_venue = {
        "name" : new_name,

        "id" : current_id,

        "image" : new_image,

        "description" : new_description,

        "rating" : new_rating,

        "reviews" : []
    }

    venues.append(new_venue);
    current_id += 1;

    return jsonify(id = new_venue["id"])

@app.route('/delete_review', methods=['POST'])
def delete_venue():
    global venues

    json_data = request.get_json()
    id = json_data["id"]
    review_id = json_data["review_id"]
    venue = None;

    for i in venues:
        if str(i["id"]) == id:
            venue = i;
            break;

    for j in venue["reviews"]:
        if str(j["id"]) == review_id:
            j["mark_as_deleted"] = True;
            break;

    return jsonify(venue = venue)

@app.route('/undo_review', methods=['POST'])
def undo_venue():
    global venues

    json_data = request.get_json()
    id = json_data["id"]
    review_id = json_data["review_id"]
    venue = None;

    for i in venues:
        if str(i["id"]) == id:
            venue = i;
            break;

    for j in venue["reviews"]:
        if str(j["id"]) == review_id:
            j["mark_as_deleted"] = False;
            break;

    return jsonify(venue = venue)

@app.route('/edit/<id>')
def edit(id=None):
    global venues
    venue = {}

    for i in venues:
        if id == str(i["id"]):
            venue = i;

    return render_template('edit_page.html', id=id, venue = venue, venues=venues)

@app.route('/update_rating', methods=['POST'])
def update_rating():
    global venues

    json_data = request.get_json()
    id = json_data["id"]
    rating = json_data["rating"]
    venue = {}

    for i in venues:
        if id == str(i["id"]):
            i["rating"] = rating;
            venue = i

    return jsonify(venue=venue)


@app.route('/update_review', methods=['POST'])
def update_review():
    global venues
    venue = {}

    json_data = request.get_json()
    id = json_data["id"]
    user = json_data["user"]
    review = json_data["review"]

    new_review = {
        "user" : user,
        "review" : review
    }

    for i in venues:
        if id == str(i["id"]):
            new_review = {
                "id" : i['current_review_id'],
                "mark_as_deleted": False,
                "user" : user,
                "review" : review
            };
            i["reviews"].insert(0, new_review)
            i['current_review_id'] = i['current_review_id']+1;
            venue = i;

    return jsonify(venue = venue)

if __name__ == '__main__':
   app.run(debug = True)
