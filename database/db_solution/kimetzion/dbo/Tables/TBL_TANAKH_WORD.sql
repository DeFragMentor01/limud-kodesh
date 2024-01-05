﻿CREATE TABLE [dbo].[TBL_TANAKH_WORD] (
    [WORD_ID]        INT            IDENTITY (1, 1) NOT NULL,
    [PEREK_PASUK_ID] INT            NOT NULL,
    [WORD_POSITION]  INT            NOT NULL,
    [IS_KTIV]        BIT            NOT NULL,
    [IS_KRI]         BIT            NOT NULL,
    [WORD]           NVARCHAR (100) NOT NULL,
    [FULL_WORD]      NVARCHAR (100) NOT NULL,
    CONSTRAINT [PK_TBL_TANAKH_WORD_WORD_ID] PRIMARY KEY CLUSTERED ([WORD_ID] ASC),
    CONSTRAINT [FK_TBL_TANAKH_WORD_PEREK_PASUK_ID] FOREIGN KEY ([PEREK_PASUK_ID]) REFERENCES [dbo].[TBL_TANAKH_PEREK_PASUK] ([PEREK_PASUK_ID])
);
