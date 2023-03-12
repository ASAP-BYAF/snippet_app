const createForm = document.getElementById('snippet-create');
const langList = createForm.lang
const typeList = createForm.type
const newLangField = document.getElementById('id_lang_new');
const newTypeField = document.getElementById('id_type_new');
createForm.addEventListener('change', handleChange);

function handleChange() {
    for (let i_lang=0; i_lang<langList.length; i_lang++) {
        const i_opt = langList[i_lang];
        if (i_opt.checked) {
            for (let j_type=0; j_type<typeList.length-1; j_type++) {
                const j_opt = typeList[j_type];
                if (i_opt.value == j_opt.value.split('.')[0]){
                    displayField(true, j_opt.parentElement);
                } else {
                    displayField(false, j_opt.parentElement);
                    j_opt.checked = false;
                }
            }
        }
        if (i_opt.value == 0) {
            displayField(i_opt.checked, newLangField);
            if (i_opt.checked) {
                typeList[typeList.length-1].checked = true;
            }
        }
        displayField(typeList[typeList.length-1].checked, newTypeField)
    }
}

function displayField(ifDisplay, target){
  if(ifDisplay){
      target.style.display= "block";
  } else {
      target.style.display= "None";
  }
}
