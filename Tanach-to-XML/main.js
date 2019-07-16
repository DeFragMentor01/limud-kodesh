var fs = require('fs')


fs.readdir('./all_tanach_in_text', (err, dataTxt) => {
    if (err) throw err;
    for (var txt in dataTxt) {
        var data = fs.readFileSync(`./all_tanach_in_text/${dataTxt[txt]}`)

        var newdata = JSON.parse(data)

        var file_no_extension = dataTxt[txt].replace(/\.[^\.]+$/, '')

        var result = [];

        for (var i in newdata) {
            result.push([newdata[i]]);

        }

        var result2 = []

        var stmt = '';

        for (var i in result) {

            for (var a in result[i]) {

                for (var e in result[i][a]) {
                    for (var z in result[i][a][e]) {
                        var numberLineChapter= result[i][a][e].length -1
                        result2.push(result[i][a][e][z].split(','))
                        var sentence = result[i][a][e][z].split(' ');
                        for (var w in sentence) {
                            for( var l in sentence[w]){
                                if(sentence[w][l] == '-'){
                                    
                                }
                            }
                            if (z == 0 && w == 0) {
                                stmt += `<Word Book='${file_no_extension}' StartPerekBeforeWord='true' Chapter='${1 + parseInt(e)}' Verse='${parseInt(z) + 1}' WordSequence='${parseInt(w) + 1}'>${sentence[w]}</Word>${'\n\r'}`
                                continue
                            }
                            if (z == numberLineChapter && w == sentence.length -1) {
                                continue
                            }
                            else{
                                if(sentence[w] == '(פ)'){
                                    stmt += `<Word Book='${file_no_extension}' Chapter='${1 + parseInt(e)}' Verse='${parseInt(z) + 1}' WordSequence='${parseInt(w) + 1}' IsParashaPtuchah='true'>${sentence[w]}</Word>${'\n\r'}`
                                    continue
                                }
                                stmt += `<Word Book='${file_no_extension}' Chapter='${1 + parseInt(e)}' Verse='${parseInt(z) + 1}' WordSequence='${parseInt(w) + 1}'>${sentence[w]}</Word>${'\n\r'}`

                            }                            

                        }
                    }
                    if(sentence[w] == '(פ)'){
                        stmt += `<Word Book='${file_no_extension}' EndPerekAfterWord='true' Chapter='${Number(e) + 1}' Verse='${Number(z) + 1}' WordSequence='${sentence.length}' IsParashaPtuchah='true'>${sentence[w]}</Word>${'\n\r'}`
                        continue
                    }
                    stmt += `<Word Book='${file_no_extension}' EndPerekAfterWord='true' Chapter='${Number(e) + 1}' Verse='${Number(z) + 1}' WordSequence='${sentence.length}'>${sentence[w]}</Word>${'\n\r'}`

                }
            }
        }



        var FinalStatement = `<Tanakh>${'\n\r'}${stmt}</Tanakh>`
        var file = dataTxt[txt].replace(/\.[^\.]+$/, '.xml');

        // fs.writeFile(`./Tanach-xml/${file}`, FinalStatement, (err) => {
        //     if (err) throw err
        // })
    }
});



