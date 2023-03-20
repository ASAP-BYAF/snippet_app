const createForm = document.getElementById('snippet-create');
const langList = createForm.lang
const typeList = createForm.type
const newLangField = document.getElementById('id_new_lang');
const newTypeField = document.getElementById('id_new_type');

createForm.addEventListener('change', handleChange);
window.addEventListener("load", handleChange);

function handleChange() {
    for (let i_lang=0; i_lang<langList.length; i_lang++) {
        const i_opt = langList[i_lang];
        if (i_opt.checked) {
            for (let j_type=0; j_type<typeList.length-1; j_type++) {
                const j_opt = typeList[j_type];
                if (i_opt.value == j_opt.value.split('.')[0]){
                    handleDisplay(true, j_opt.parentElement);
                } else {
                    handleDisplay(false, j_opt.parentElement);
                    j_opt.checked = false;
                }
            }
        }
        if (i_opt.value == 0) {
            handleDisplay(i_opt.checked, newLangField);
            handleRequired(i_opt.checked, newLangField.lastElementChild);
            if (i_opt.checked) {
                typeList[typeList.length-1].checked = true;
            }
        }
    }
    handleDisplay(typeList[typeList.length-1].checked, newTypeField)
    handleRequired(typeList[typeList.length-1].checked, newTypeField.lastElementChild)
}

function handleDisplay(ifDisplay, target){
  if(ifDisplay){
      target.style.display= "block";
  } else {
      target.style.display= "None";
  }
}

function handleRequired(ifRequired, target){
  if(ifRequired){
      target.required=true;
  } else {
      target.required=false;
  }
}