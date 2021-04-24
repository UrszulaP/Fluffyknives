insert into item values (
    1,
    'Red elegance',
    'Klasyka i elegancja, wszechstronność zastosowania, wykute w jednym nożu.',
    '<ul><li>długość całkowita: 17cm</li><li>ostrze ze stali szybkotnącej</li><li>rączka w kolorze czerwonym</li></ul>',
    'noz1.jpg', 299.0
);
insert into item values (
    2,
    'Hunter',
    'Nóż dla wymagających. Wytrzymałe ostrze o zwiększonej grubości. Klasyczna czerń.',
    '<ul><li>długość całkowita: 22cm</li><li>ostrze 4mm ze stali szybkotnącej</li><li>rączka w kolorze czarnym</li></ul>',
    'noz2.jpg', 379.0
);
insert into item values (
    3,
    'Pocket blade',
    'Poręczny nożyk w wersji mini. Srebrne wykończenie ostrza.',
    '<ul><li>długość całkowita: 13cm</li><li>ostrze ze stali szybkotnącej</li><li>rączka w kolorze czerwono-czarnym</li></ul>',
    'noz3.jpg', 249.0
);
insert into item values (
    4,
    'Hunter + pokrowiec',
    'Nóż dla wymagających. Wytrzymałe ostrze o zwiększonej grubości. Klasyczna czerń. W komplecie pokrowiec z naturalnej skóry.',
    '<ul><li>długość całkowita: 22cm</li><li>ostrze 4mm ze stali szybkotnącej</li><li>rączka w kolorze czarnym</li></ul>',
    'noz4.jpg', 499.0
);
insert into item values (
    5,
    'Red elegance L',
    'Klasyka i elegancja, wszechstronność zastosowania, wykute w jednym nożu. Wersja o zwiększonej długości rączki.',
    '<ul><li>długość całkowita: 20cm</li><li>ostrze ze stali szybkotnącej</li><li>rączka w kolorze czerwonym</li></ul>',
    'noz5.jpg', 299.0
);
insert into item values (
    6,
    'Ruby snake',
    'Wytrzymałość i oryginalny design. Ostrze o zwiększonej grubości. Rączka czerwono-czarna "skóra węża".',
    '<ul><li>długość całkowita: 22cm</li><li>ostrze 4mm ze stali szybkotnącej</li><li>rączka: czerwono-czarna siatka</li></ul>',
    'noz6.jpg', 359.0
);



insert into user values (
    1,
    'Admin',
    'admin@admin.admin',
    '$2b$12$GXZu.Aml.PCt7x5LtdWuk.FpyMVT6jRWVw4C04rJT/MtHZn1UC4pO',
    'defaultpp.jpg', null, null, 1
);
insert into user values (
    2,
    'Ula',
    'ula@ula.ula',
    '$2b$12$XeU4aQLX9gCsv/9emucoEOWv4V4Aiz2ufU7XqRJXpxZdH57Bvvg1i',
    '2d7dd1729f243bfc.jpg',
    'ul. Prosta 1/2, 12-345 Piaski',
    '609 756 678', 0
);
insert into user values (
    3,
    'Ania',
    'ania@ania.ania',
    '$2b$12$6YNxHGpkbZazc6wUtL3STOHFkubRC4epy/aK9iWtxRKSbPW99yc1a',
    'defaultpp.jpg',
    'ul. Długa 2/8, 14-366 Łuków',
    '609 226 167', 0
);
insert into user values (
    4,
    'Kuba',
    'kuba@kuba.kuba',
    '$2b$12$tKsfnvivjkdvIS5/4/ZqlO27s6QMMluWA9Nd1O6VzEI/y6di9.jWe',
    'db01140513d3fe64.jpg',
    'ul. Spadochroniarzy 3, 14-495 Siedlce',
    '743 267 736', 0
);



insert into 'order' values (
    1, 5, 4,
    'Dostarczono'
);
insert into 'order' values (
    2, 4, 4,
    'Wysłano'
);
insert into 'order' values (
    3, 1, 2,
    'Dostarczono'
);
insert into 'order' values (
    4, 4, 3,
    'Wysłano'
);
insert into 'order' values (
    5, 6, 2,
    'Wysłano'
);
insert into 'order' values (
    6, 3, 4,
    'W trakcie realizacji'
);
insert into 'order' values (
    7, 1, 3,
    'Dostarczono'
);
insert into 'order' values (
    8, 2, 2,
    'W trakcie realizacji'
);
