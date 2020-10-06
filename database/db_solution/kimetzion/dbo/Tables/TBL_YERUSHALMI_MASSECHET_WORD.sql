﻿CREATE TABLE [dbo].[TBL_YERUSHALMI_MASSECHET_WORD] (
    [YERUSHALMI_WORD_ID]   INT           IDENTITY (1, 1) NOT NULL,
    [MASSECHET_HALACHA_ID] INT           NOT NULL,
    [WORD_TYPE]            BIT           NOT NULL,
    [WORD]                 NVARCHAR (50) NOT NULL,
    [WORD_POSITION]        INT           NOT NULL,
    [W_DELETED]            BIT           NOT NULL,
    [W_ADDED]              BIT           NOT NULL,
    CONSTRAINT [PK_TBL_YERUSHALMI_MASSECHET_WORD] PRIMARY KEY CLUSTERED ([YERUSHALMI_WORD_ID] ASC),
    CONSTRAINT [FK_TBL_YERUSHALMI_MASSECHET_WORD_MASSECHET_HALACHA_ID] FOREIGN KEY ([MASSECHET_HALACHA_ID]) REFERENCES [dbo].[TBL_YERUSHALMI_MASSECHET_HALACHA] ([MASSECHET_HALACHA_ID])
);

