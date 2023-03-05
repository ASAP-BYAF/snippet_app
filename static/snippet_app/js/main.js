const createForm = document.getElementById('snippet-create');
const langList = createForm.lang
const typeList = createForm.type
const newLangField = document.getElementById('id_lang_new');
const newTypeField = document.getElementById('id_type_new');
createForm.addEventListener('change', handleChange);

console.log(langList);

function handleChange() {
        for (let i=0; i<langList.length; i++) {
            const i_opt = langList[i];
            if (i_opt.value == 0) {
                displayField(i_opt.checked, newLangField);
                displayField(i_opt.checked, newTypeField);
            }
        }
}

function displayField(ifDisplay, target){
  if(ifDisplay){
      target.style.display= "block";
  } else {
      target.style.display= "None";
  }
}