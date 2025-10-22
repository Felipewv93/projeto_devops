CREATE TABLE filmes (

    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    diretor VARCHAR(50) NOT NULL,
    estudio VARCHAR(100) NOT NULL,
    genero VARCHAR(50) NOT NULL,
    ano INT NOT NULL,
    bilheteria BIGINT NOT NULL
);

INSERT INTO filmes (titulo, diretor, estudio, genero, ano, bilheteria)
VALUES

    ('Avatar', 'James Cameron', '20th Century Fox', 'Ficção Científica', 2009, 2923710708),
    ('Avengers: Endgame', 'Anthony e Joe Russo', 'Marvel Studios', 'Super-herói', 2019, 2799439100),
    ('Avatar: The Way of Water', 'James Cameron', '20th Century Studios', 'Ficção Científica', 2022, 2343068977),
    ('Titanic', 'James Cameron', '20th Century Fox', 'Romance', 1997, 2264812968),
    ('Ne Zha 2', 'Jiaozi', 'Beijing Enlight Pictures', 'Animação', 2025, 2150000000),
    ('Star Wars: Episode VII - The Force Awakens', 'J.J. Abrams', 'Lucasfilm', 'Ficção Científica', 2015, 2071310218),
    ('Avengers: Infinity War', 'Anthony e Joe Russo', 'Marvel Studios', 'Super-herói', 2018, 2052415039),
    ('Spider-Man: No Way Home', 'Jon Watts', 'Columbia Pictures/Marvel Studios', 'Super-herói', 2021, 1921426073),
    ('Inside Out 2', 'Kelsey Mann', 'Pixar Animation Studios', 'Animação', 2024, 1698863816),
    ('Jurassic World', 'Colin Trevorrow', 'Universal Pictures', 'Aventura', 2015, 1671537444),
    ('The Lion King (2019)', 'Jon Favreau', 'Walt Disney Pictures', 'Animação', 2019, 1662020819),
    ('The Avengers', 'Joss Whedon', 'Marvel Studios', 'Super-herói', 2012, 1520538536),
    ('Furious 7', 'James Wan', 'Universal Pictures', 'Ação', 2015, 1515342457),
    ('Top Gun: Maverick', 'Joseph Kosinski', 'Paramount Pictures', 'Ação', 2022, 1495696292),
    ('Frozen II', 'Chris Buck e Jennifer Lee', 'Walt Disney Animation Studios', 'Animação', 2019, 1453683476),
    ('Barbie', 'Greta Gerwig', 'Warner Bros. Pictures', 'Comédia', 2023, 1447138421),
    ('Avengers: Age of Ultron', 'Joss Whedon', 'Marvel Studios', 'Super-herói', 2015, 1405018048),
    ('The Super Mario Bros. Movie', 'Aaron Horvath e Michael Jelenic', 'Illumination Entertainment', 'Animação', 2023, 1360847665),
    ('Black Panther', 'Ryan Coogler', 'Marvel Studios', 'Super-herói', 2018, 1349926083),
    ('Harry Potter and the Deathly Hallows: Part 2', 'David Yates', 'Warner Bros. Pictures', 'Fantasia', 2011, 1342505340);