document.getElementById('downloadBtn').addEventListener('click', function () {
    const summaryText = document.getElementById('summary').innerText;
    const opt = {
        margin: 0.5,
        filename: 'summary.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    const element = document.getElementById('summary').parentElement.parentElement.parentElement;
    print(element);
    html2pdf().from(element).set(opt).save();
});