window.addEventListener('DOMContentLoaded', (event) => {
    main();
});
function main() {
    var today = new Date().getHours();
    if (today <= 6 || today >= 22) {
        alert('It is after 10 p.m. Unless your prayer request is urgent, please be courteous and wait until morning. Thanks!');
    }
    getQuote();
}
function getQuote() {
    document.getElementById("reloadbtn").classList.toggle("fa-spin")
    setTimeout(() => {
        document.getElementById("reloadbtn").classList.toggle("fa-spin")
    }, 1000);
    var quotes = [
        {
            text: "Ask and you will receive; seek and you will find; knock and the door will be opened to you.",
            verse: "Luke 11:9"
        },
        {
            text: "Rejoice always, pray continually, give thanks in all circumstances; for this is God’s will for you in Christ Jesus.",
            verse: '1 Thessalonians 5:16-18',
        },
        {
            text: "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
            verse: "Philippians 4:6-7",
        },
        {
            text: 'This is the confidence we have in approaching God: that if we ask anything according to his will, he hears us.',
            verse: '1 John 5:14'
        }, {
            text: 'Devote yourselves to prayer, being watchful and thankful.', verse: 'Collosians 4:2'
        },
        {
            text: 'Then you will call on me and come and pray to me, and I will listen to you.',
            verse: 'Jeremiah 29:12'
        },
        {
            text: 'To be a Christian without prayer is no more possible than to be alive without breathing',
            verse: 'Martin Luther'
        },
        {
            text: 'Our prayers may be awkward. Our attempts may be feeble. But since the power of prayer is in the one who hears it and not the one who says it, our prayers do make a difference.',
            verse: 'Max Lucado'

        },
        {
            text: 'Any concern too small to be turned to in prayer is too small to be made into a burden',
            verse: 'Corrie Ten Boom'
        }
    ];
    var quote = quotes[Math.floor(Math.random() * quotes.length)];
    if (screen.width > 650) {
        document.getElementById("quote").innerHTML =
            '<h2><i>"' + quote.text + '"</i></h2>' +
            '<cite>' + quote.verse + '</cite>'
            ;
    }
}
