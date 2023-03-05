alert('hello world');

//const langList = document.getElementById('id_lang');
const langList = document.getElementById('snippet-create');
langList.addEventListener('change', handleChange);

function handleChange() {
    const langVal = langList.lang.value;
    console.log(langList);
    console.log(langList.lang);
    console.log(langVal);
    console.log('test');
}