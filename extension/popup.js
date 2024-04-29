document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("summarise");

    if (btn) {
        btn.addEventListener("click", function () {
            btn.disabled = true;
            btn.innerHTML = "Summarising...";

            chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
                var url = tabs[0].url;
                var xhr = new XMLHttpRequest();
                if (url.startsWith("https://www.youtube.com/")) {
                    xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + url, true);
                } else{
                    print("inside article")
                    xhr.open("GET", "http://127.0.0.1:5000/article?url=" + url, true);

                }


                xhr.onload = function () {
                    var text = xhr.responseText;
                    var summaryWindow = window.open('summary.html', '_blank');

                    summaryWindow.onload = function () {
                        summaryWindow.document.getElementById("summary").textContent = text;


                        btn.disabled = false;
                        btn.innerHTML = "Summarise";
                    };
                };

                xhr.send();
            });
        });
    } else {
        console.error("Element with id 'summarise' not found.");
    }
});