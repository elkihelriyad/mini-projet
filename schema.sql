DROP TABLE IF EXISTS filieres;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS users;

CREATE TABLE filieres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    nom TEXT NOT NULL,
    description TEXT NOT NULL,
    debouches TEXT,
    mots_cles TEXT,
    formation_json TEXT
);

CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texte TEXT NOT NULL,
    texte_en TEXT,
    texte_ar TEXT,
    dimensions TEXT NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    access_code TEXT NOT NULL,
    nom_complet TEXT,
    last_result_json TEXT,
    profile_type TEXT,
    date_test DATETIME
);

INSERT INTO users (email, access_code, nom_complet) VALUES
('etudiant@uca.ac.ma', '123456', 'Etudiant Test'),
('ahmed@uca.ac.ma', 'ENSAS2026', 'Ahmed Haloubi'),
('o.elmessaoudi@uca.ac.ma', 'GENIE2026', 'Othmane El Messaoudi'),
('r.elkihel@uca.ac.ma', 'INFO2026', 'Riyad El Kihel'),
('a.haloubi@uca.ac.ma', 'DATA2026', 'Ahmed Haloubi');

INSERT INTO filieres (code, nom, description, debouches, mots_cles, formation_json) VALUES
('GIIA', 'Génie Informatique et Intelligence Artificielle', 
'<strong>Option 1 : GÉNIE INFORMATIQUE</strong><br>L’option Ingénierie Informatique et Décisionnelle de l’ENSA-Safi répond à une demande nationale
et régionale croissante des ingénieurs en développement informatique et l’informatique
décisionnelle dans les différents secteurs industriels et de services, notre filière souhaite ainsi doter
le tissu économique national et régional de cadre opérationnel dans les métiers de l’informatique,
en développement, réseaux, base de données et sécurité informatique et en informatique
décisionnelle. Ces vastes domaines, toujours en constante évolution, constitue l’objectif d’un
ensemble d’enseignements techniques et scientifiques, d’autres modules complémentaires (sciences
humaines, managements...), visent à permettre à d’autre demandes et besoins croissants où le profil
d’ingénieur s’impose, de par ses connaissances, ses aptitudes, sa rigueur. Il s’agit de secteurs
d’activités liés au tertiaire avancé, qu’il soit public ou privé et où les technologies de l’information
constituent un outil incontournable dont on ne pourrait plusse passer.
Elles sont dispensées durant les quatre derniers semestres. S’y ajoutent, des matières et des cours
spécifiques permettant de caractériser la formation 8 / 303 propre à la filière informatique et
réseaux et ses orientations. Elles font l’objet d’un enseignement durant les trois derniers semestres.<br><br><strong>Option 2 : INGÉNIERIE DES DONNÉES ET INTELLIGENCE ARTIFICIELLE</strong><br>"L''objectif principal de l’option IDIA est de former des ingénieurs, de haut niveau scientifique
équilibré entre la théorie et la pratique, capables de récupérer, stocker, organiser et traiter de
grandes masses d’informations, afin de faciliter leur compréhension et permettre aux dirigeants
d''adopter les bonnes stratégies. Les lauréats de la filière IDIA sont par conséquent des acteur-clés
pour la gestion de grandes sociétés. Techniquement parlant, la filière IDIA répond à une forte
demande du marché du travail pour des compétences en technologies Big data, Datamining,
intelligence artificielle et internet des objets. Elle constitue également une contribution à la
concrétisation de la vision du Maroc à explorer les techniques de l’intelligence artificielle, afin de
développer efficacement différents domaines socio-économiques."',

'Data analyst/mineur, Data Scientist, Développeur Big data, Data manager, Architecte Big Data, Ingénieur Big Data, Développeur IA, Consultant IA, Business Developer, Responsable marketing IA, Chef de projet d''innovation, Chef de projet Chatbot, Ingénieur IoT, Ingénieur système, Administrateur de bases de données, Ingénieur d''études, Expert en technologie internet / multimédia, Consultant en informatique décisionnelle, etc.',
'Systèmes d''Information, Blockchain, Data Science, Big Data, Systèmes Intelligents, Machine Learning, Base De Données Nosql, Multimédia Mining, Réseaux, Cloud Computing, Système Hadoop, Deep Learning, Sécurité, Data Mining, informatique, Cybersécurité, Virtualisation, conception web..., Intelligence artificielle, Objets connectés et IOT, Développement informatique, Application de l''intelligence artificielle et Data Science aux systèmes de l''information et de communication.',
'[
    {
        "year": "1ère Année",
        "semesters": [
            {
                "name": "Semestre 1",
                "modules": ["Ingénierie Financière", "Mathématiques pour l''Ingénieur", "Python pour la Data Science et le Machine Learning", "Systèmes d''Information", "Modélisation Stochastique", "Systèmes de Gestion de Contenu", "LC 1"]
            },
            {
                "name": "Semestre 2",
                "modules": ["Transition Écologique et Dynamiques Culturelles", "Techniques d''Optimisation Avancées", "Systèmes d''Exploitation et Environnements de Développement", "Modélisation UML", "Architecture des Systèmes", "Machine Learning", "LC 2"]
            }
        ]
    },
    {
        "year": "2ème Année",
        "semesters": [
            {
                "name": "Semestre 3",
                "modules": ["Développement Backend en JS", "Marketing et Développement Durable", "Bases de Données Avancées", "Méthodes Heuristiques et Méta-Heuristiques", "Projets Tutorés", "Analyse des Données", "Programmation Java Avancée", "Développement Web Dynamique", "LC 3"]
            },
            {
                "name": "Semestre 4",
                "modules": ["Gouvernance des Systèmes d''Information", "Génie Logiciel", "Systèmes Intelligents Flous", "Traitement d''Image / Vision Artificielle", "Internet des Objets", "Cloud Computing et Virtualisation", "Introduction à la Sécurité des Réseaux et Systèmes", "Management de Projet et Entrepreneuriat", "LC 4"]
            }
        ]
    },
    {
        "year": "3ème Année",
        "semesters": [
            {
                "name": "Semestre 5",
                "modules": ["Architectures Réparties JEE", "Ingénierie des Données Massives et Big Data", "Anglais", "Traitement Automatique du Langage Naturel", "Théorie des Jeux et Systèmes Multi-Agents", "Web Sémantique et Développement Mobile"]
            },
            {
                "name": "Semestre 6",
                "modules": ["Intégration et Solutions Métiers", "E-Management et Innovation / Innovation et Entrepreneuriat", "Sécurité des Systèmes d''Information et Technologie Blockchain", "Factory Management / Usine de Développement Logiciel", "Projet de Fin d''Études"]
            }
        ]
    }
]'),
('GTR', 'Génie Réseaux & Télécom', 'Réseaux, 5G, Sécurité, IoT', NULL, NULL, NULL),
('GINDUS', 'Génie Industriel', 'Logistique, Supply Chain, Qualité', NULL, NULL, NULL),
('GMSI', 'Génie Mécatronique et Systèmes Intelligents', 'Robotique, Électronique, Automatisme', NULL, NULL, NULL),
('GPMA', 'Génie des Procédés & Matériaux Avancés', 'Chimie, Matériaux, Environnement', NULL, NULL, NULL),
('GATE', 'Génie Aéronautique et Technologies de l''Espace', 'Aéronautique, Maintenance, Conception', NULL, NULL, NULL);

INSERT INTO questions (texte, texte_en, texte_ar, dimensions) VALUES
('J’aime organiser et améliorer le fonctionnement d’une entreprise.', 'I like organizing and improving the operations of a company.', 'أحب تنظيم وتحسين سير عمل الشركة.', 'D5,D6'),
('J’aime résoudre des problèmes mathématiques.', 'I love solving mathematical problems.', 'أحب حل المشكلات الرياضية.', 'D1'),
('Je m’intéresse à la façon dont l’information est transmise entre des appareils.', 'I am interested in how information is transmitted between devices.', 'أهتم بكيفية انتقال المعلومات بين الأجهزة.', 'D3'),
('J’aime programmer et développer des applications numériques.', 'I love programming and developing digital applications.', 'أحب البرمجة وتطوير التطبيقات الرقمية.', 'D2'),
('Je m’intéresse à la manière dont les matériaux sont créés et améliorés.', 'I am interested in how materials are created and improved.', 'أهتم بكيفية إنشاء المواد وتحسينها.', 'D5'),
('J’aime travailler en équipe sur des projets complexes.', 'I like working in a team on complex projects.', 'أحب العمل ضمن فريق في مشاريع معقدة.', 'D6'),
('J’aime comprendre comment les systèmes de communication relient les personnes et les appareils.', 'I like understanding how communication systems connect people and devices.', 'أحب فهم كيف تربط أنظمة الاتصال الأشخاص والأجهزة.', 'D3'),
('Je préfère les projets pratiques où je construis et teste des systèmes.', 'I prefer hands-on projects where I build and test systems.', 'أفضل المشاريع العملية حيث أقوم ببناء واختبار الأنظمة.', 'D4'),
('Je suis curieux(se) de comprendre comment de grandes quantités de données aident à prendre des décisions.', 'I am curious to understand how large amounts of data help in decision-making.', 'أنا فضولي لفهم كيف تساعد كميات كبيرة من البيانات في اتخاذ القرارات.', 'D2,D6'),
('Je suis attiré(e) par les secteurs liés aux transports avancés ou à l’aéronautique.', 'I am attracted to sectors related to advanced transport or aeronautics.', 'أنجذب إلى القطاعات المتعلقة بالنقل المتقدم أو الطيران والفضاء.', 'D4'),
('J’aime analyser les coûts, l’efficacité et la performance d’une organisation.', 'I like analyzing the costs, efficiency, and performance of an organization.', 'أحب تحليل التكاليف والكفاءة وأداء المؤسسة.', 'D5,D6'),
('J’aime analyser et améliorer les processus de production industrielle.', 'I like analyzing and improving industrial production processes.', 'أحب تحليل وتحسين عمليات الإنتاج الصناعي.', 'D5'),
('J’aime concevoir des systèmes numériques ou des solutions web.', 'I love designing digital systems or web solutions.', 'أحب تصميم الأنظمة الرقمية أو حلول الويب.', 'D2'),
('Je m’intéresse aux robots ou aux machines intelligentes.', 'I am interested in robots or intelligent machines.', 'أهتم بالروبوتات أو الآلات الذكية.', 'D4'),
('Je suis sensible à la protection des systèmes numériques et des informations.', 'I am concerned about protecting digital systems and information.', 'أهتم بحماية الأنظمة الرقمية والمعلومات.', 'D2,D8'),
('Je me sens à l’aise pour appliquer les mathématiques et la physique à des problèmes concrets.', 'I feel comfortable applying mathematics and physics to concrete problems.', 'أشعر بالارتياح عند تطبيق الرياضيات والفيزياء على مشكلات ملموسة.', 'D1'),
('J’intéresse à la gestion de projets et à la coordination d’équipes.', 'I am interested in project management and team coordination.', 'أهتم بإدارة المشاريع وتنسيق الفرق.', 'D6'),
('J’aime comprendre comment fonctionnent les avions ou les véhicules complexes.', 'I like understanding how planes or complex vehicles work.', 'أحب فهم كيفية عمل الطائرات أو المركبات المعقدة.', 'D4'),
('J’aime résoudre des problèmes logiques à l’aide d’algorithmes.', 'I like solving logical problems using algorithms.', 'أحب حل المشكلات المنطقية باستخدام الخوارزميات.', 'D1,D2'),
('Je m’intéresse aux technologies modernes de communication et aux objets connectés.', 'I am interested in modern communication technologies and connected objects.', 'أهتم بتقنيات الاتصال الحديثة والأشياء المتصلة.', 'D3'),
('Je suis sensible aux questions d’énergie et d’impact environnemental dans l’industrie.', 'I am concerned about energy issues and environmental impact in industry.', 'أهتم بقضايا الطاقة والتأثير البيئي في الصناعة.', 'D5,D8'),
('J’aime concevoir des systèmes utilisant des capteurs ou des dispositifs automatisés.', 'I like designing systems using sensors or automated devices.', 'أحب تصميم أنظمة تستخدم أجهزة استشعار أو أجهزة آلية.', 'D4'),
('Je me sens à l’aise pour prendre des décisions qui tiennent compte des aspects techniques et économiques.', 'I feel comfortable making decisions that consider both technical and economic aspects.', 'أشعر بالارتياح لاتخاذ قرارات تأخذ في الاعتبار الجوانب التقنية والاقتصادية.', 'D6'),
('J’aime analyser des signaux ou des informations numériques.', 'I like analyzing digital signals or information.', 'أحب تحليل الإشارات الرقمية أو المعلومات.', 'D2,D3'),
('Je m’intéresse à l’intelligence artificielle et à l’analyse des données.', 'I am interested in artificial intelligence and data analysis.', 'أهتم بالذكاء الاصطناعي وتحليل البيانات.', 'D2'),
('J’aime résoudre des problèmes techniques à l’aide de modèles ou de simulations.', 'I like solving technical problems using models or simulations.', 'أحب حل المشكلات التقنية باستخدام النماذج أو المحاكاة.', 'D1,D7'),
('Je m’intéresse à la logistique, à la planification de production ou à la gestion des flux.', 'I am interested in logistics, production planning, or flow management.', 'أهتم باللوجستيات أو تخطيط الإنتاج أو إدارة التدفقات.', 'D5'),
('Je me sens à l’aise pour utiliser des données afin d’améliorer les performances d’un système de production.', 'I feel comfortable using data to improve the performance of a production system.', 'أشعر بالارتياح لاستخدام البيانات لتحسين أداء نظام الإنتاج.', 'D2,D5'),
('Je m’intéresse à l’amélioration de la performance et de la fiabilité des systèmes techniques.', 'I am interested in improving the performance and reliability of technical systems.', 'أهتم بتحسين أداء وموثوقية الأنظمة التقنية.', 'D8'),
('Je suis attiré(e) par les technologies innovantes en informatique.', 'I am attracted to innovative technologies in computer science.', 'أنجذب إلى التقنيات المبتكرة في علوم الكمبيوتر.', 'D2'),
('J’aime comprendre comment les matières premières sont transformées en produits finis.', 'I like understanding how raw materials are transformed into finished products.', 'أحب فهم كيفية تحويل المواد الخام إلى منتجات نهائية.', 'D5'),
('J’aime travailler avec des systèmes qui gèrent de grandes quantités d’informations.', 'I like working with systems that manage large amounts of information.', 'أحب العمل مع الأنظمة التي تدير كميات كبيرة من المعلومات.', 'D2'),
('Je m’intéresse aux technologies intelligentes et automatisées.', 'I am interested in smart and automated technologies.', 'أهتم بالتقنيات الذكية والآلية.', 'D4'),
('Je préfère améliorer un système existant plutôt que d’en inventer un totalement nouveau.', 'I prefer improving an existing system rather than inventing a completely new one.', 'أفضل تحسين نظام موجود بدلاً من اختراع نظام جديد تمامًا.', 'D5,D8'),
('Je m’intéresse aux systèmes techniques complexes qui exigent un haut niveau de sécurité.', 'I am interested in complex technical systems that require a high level of security.', 'أهتم بالأنظمة التقنية المعقدة التي تتطلب مستوى عالٍ من الأمان.', 'D8'),
('J’aime comprendre comment sont organisés les systèmes de production industrielle.', 'I like understanding how industrial production systems are organized.', 'أحب فهم كيفية تنظيم أنظمة الإنتاج الصناعي.', 'D5'),
('J’aime travailler avec des machines et des équipements techniques.', 'I like working with machines and technical equipment.', 'أحب العمل مع الآلات والمعدات التقنية.', 'D4'),
('J’aime lire des articles scientifiques ou techniques.', 'I like reading scientific or technical articles.', 'أحب قراءة المقالات العلمية أو التقنية.', 'D7'),
('Je suis intéressé(e) par la recherche pour mieux comprendre le fonctionnement des choses.', 'I am interested in research to better understand how things work.', 'أهتم بالبحث لفهم كيفية عمل الأشياء بشكل أفضل.', 'D7'),
('J’aime rédiger des rapports ou des comptes rendus structurés.', 'I like writing structured reports or accounts.', 'أحب كتابة التقارير أو المحاضر المنظمة.', 'D6,D7'),
('Je préfère les tâches clairement définies et bien organisées.', 'I prefer clearly defined and well-organized tasks.', 'أفضل المهام المحددة بوضوح والمنظمة جيدًا.', 'D5,D6'),
('J’aime diriger ou coordonner un groupe pour réaliser un projet.', 'I like leading or coordinating a group to carry out a project.', 'أحب قيادة أو تنسيق مجموعة لإنجاز مشروع.', 'D6');
