SET NOCOUNT ON;

DROP TABLE IF EXISTS TBL_INITIALS_MASSECHET_WORD

CREATE TABLE TBL_INITIALS_MASSECHET_WORD
(
IMW_ID int identity,
INITIALS_ID INT NOT NULL,
WORD_ID INT NOT NULL,
CONSTRAINT PK_TBL_INITIALS_MASSECHET_WORD_IMW_ID PRIMARY KEY (IMW_ID),
CONSTRAINT FK_TBL_INITIALS_MASSECHET_WORD_INITIALS_ID FOREIGN KEY (INITIALS_ID) REFERENCES TBL_INITIALS (INITIALS_ID),
CONSTRAINT FK_TBL_INITIALS_MASSECHET_WORD_WORD_ID FOREIGN KEY (WORD_ID) REFERENCES TBL_MASSECHET_WORD (WORD_ID)
)