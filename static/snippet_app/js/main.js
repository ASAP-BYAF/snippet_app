// snippet を作成、編集するときの処理
const createForm = document.getElementById('snippet-create');
// createForm の要素が取得できているときだけ
// 以下の処理をする。そうでないと、エラーになり、以降が実行されない。
if (createForm) {
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
    
}

// list が表示されているときのコピーボタンの設定
const copyBtn = document.getElementsByClassName('copy-btn');
if (copyBtn) {
    for (var i = copyBtn.length - 1; i >= 0; i--) {
            copyBtn[i].addEventListener("click", function(){
                
                // 選択しているテキストをクリップボードにコピーする
                navigator.clipboard.writeText(this.previousElementSibling.innerText);
                
                // コピーをお知らせする
        alert("コピーできました！" );
        });
    }
}

const searchForm = document.getElementById('snippet-search');
if (searchForm) {
    const refineList = searchForm.refine_list
    const authorInput = searchForm.author
    const filterLangInput = searchForm.filter_lang
    const filterTypeInput = searchForm.filter_type

    searchForm.addEventListener('change', handleChange);
    window.addEventListener("load", handleChange);
    
    function handleChange() {
        for (let i_refine=0; i_refine<refineList.length; i_refine++) {
            const i_opt = refineList[i_refine];
            if (i_opt.checked) {
                if (i_opt.value === 'author'){
                    displayRefineList(true);
                }
                else if (i_opt.value === 'lang_type'){
                    displayRefineList(false);
                }
            }
        }
    }

    function displayRefineList(flag) {
        for (let j_auth=0; j_auth<authorInput.length; j_auth++) {
            handleDisplay(flag, authorInput[j_auth].parentElement);
            handleRequired(flag, authorInput[j_auth]);
        }
        handleDisplay(flag, authorInput[0].parentElement.parentElement);
        handleDisplay(!flag, filterLangInput.parentElement);
        handleRequired(!flag, filterLangInput);
        handleDisplay(!flag, filterTypeInput.parentElement);
    }
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