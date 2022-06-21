function remover(input_p){
    var removerpalavra_btn = document.querySelector("button[id="+ input_p +"]"); 
    var removerpalavra_label = document.querySelector("label[id="+ input_p +"]"); 
    var removerpalavra_input = document.querySelector("input[id="+ input_p +"]");
    if (removerpalavra_btn.click) {
        removerpalavra_label.parentElement.removeChild(removerpalavra_label);
        removerpalavra_btn.parentElement.removeChild(removerpalavra_btn);
        removerpalavra_input.parentElement.removeChild(removerpalavra_input);
        
    }
}

function adicionar(){
    var newword = document.getElementById("novaspalavras").value;
    console.log(newword);
    if (newword != "" || newword != None){
    var newelement_input = document.createElement("input");
    newelement_input.setAttribute("hidden", true);
    newelement_input.setAttribute("name", "palavra");
    newelement_input.setAttribute("type", "text");
    newelement_input.setAttribute("value", newword);
    newelement_input.setAttribute("id", newword);
    console.log(newelement_input);
    var newelement_label = document.createElement("label");
    newelement_label.setAttribute("for", newword);
    newelement_label.setAttribute("id", newword);
    newelement_label.textContent=newword;
    console.log(newelement_label);
    var newelement_btn = document.createElement("button");
    newelement_btn.setAttribute("type","button");
    newelement_btn.setAttribute("class","btn btn-danger");
    newelement_btn.setAttribute("name","btnremove");
    newelement_btn.setAttribute("id", newword);
    newelement_btn.setAttribute("value", newword);
    newelement_btn.setAttribute("onclick","remover('"+newword+"')");
    newelement_btn.textContent="Remover";
    console.log(newelement_btn);
    var newelement_div=document.createElement("div");
    newelement_div.setAttribute("class","palavra");
    console.log(newelement_div);
    newelement_div.appendChild(newelement_label);
    newelement_div.appendChild(newelement_input);
    newelement_div.appendChild(newelement_btn);
    console.log(newelement_div);
    var inserirDiv=document.getElementById("palavras");
    console.log(inserirDiv);
    inserirDiv.appendChild(newelement_div);
    }
}


function removerloja(input_list){
    console.log(input_list);
    var input_l = input_list[0]
    var input_l_url = input_list[1]
    console.log(input_l);
    console.log(input_l_url);
    input_l_url = String(input_l_url)
    console.log(input_l_url)
    var removerloja_btn = document.querySelector("button[id="+ input_l +"]");
    console.log(removerloja_btn)
    var removerloja_label = document.querySelector("label[id="+ input_l +"]"); 
    var removerloja_url_label = document.querySelector("label[id2="+ input_l +"]"); 
    var removerloja_input = document.querySelector("input[id="+ input_l +"]");
    var removerloja_url_input = document.querySelector("input[id2="+ input_l +"]");
    var removerloja_div = document.querySelector("div[id="+ input_l +"]");

    if (removerloja_btn.click) {
        removerloja_label.parentElement.removeChild(removerloja_label);
        removerloja_url_label.parentElement.removeChild(removerloja_url_label);
        removerloja_btn.parentElement.removeChild(removerloja_btn);
        removerloja_input.parentElement.removeChild(removerloja_input);
        removerloja_url_input.parentElement.removeChild(removerloja_url_input);
        removerloja_div.parentElement.removeChild(removerloja_div);
    }
}

function adicionarloja(){
    var newloja = document.getElementById("novaslojas").value;
    var newlojaurl = document.getElementById("novaslojasulr").value;
    console.log(newloja,newlojaurl);
    if ((newloja != "" || newloja != None) && (newlojaurl != "" || newlojaurl != None)){
    var newlojaelement_input = document.createElement("input");
    newlojaelement_input.setAttribute("hidden", true);
    newlojaelement_input.setAttribute("name", "loja");
    newlojaelement_input.setAttribute("type", "text");
    newlojaelement_input.setAttribute("value", newloja);
    newlojaelement_input.setAttribute("id", newloja);
    console.log(newlojaelement_input);
    var newlojaurlelement_input = document.createElement("input");
    newlojaurlelement_input.setAttribute("hidden", true);
    newlojaurlelement_input.setAttribute("name", "loja url");
    newlojaurlelement_input.setAttribute("type", "text");
    newlojaurlelement_input.setAttribute("value", newlojaurl);
    newlojaurlelement_input.setAttribute("id", newlojaurl);
    newlojaurlelement_input.setAttribute("id2", newloja);
    console.log(newlojaurlelement_input);

    var newlojaelement_label = document.createElement("label");
    newlojaelement_label.setAttribute("for", newloja);
    newlojaelement_label.setAttribute("id", newloja);
    newlojaelement_label.textContent=newloja;
    console.log(newlojaelement_label);
    var newlojaelementurl_label = document.createElement("label");
    newlojaelementurl_label.setAttribute("for", newlojaurl);
    newlojaelementurl_label.setAttribute("id", newlojaurl);
    newlojaelementurl_label.setAttribute("id2", newloja);
    newlojaelementurl_label.textContent=newlojaurl;
    console.log(newlojaelementurl_label);

    var newlojaelement_btn = document.createElement("button");
    newlojaelement_btn.setAttribute("type","button");
    newlojaelement_btn.setAttribute("class","btn btn-danger");
    newlojaelement_btn.setAttribute("name","btnremoveloja");
    newlojaelement_btn.setAttribute("id", newloja);
    newlojaelement_btn.setAttribute("id2", newlojaurl);
    newlojaelement_btn.setAttribute("value", newloja);
    newlojaelement_btn.setAttribute("onclick","removerloja(['"+newloja+"','"+newlojaurl+"'])")
    newlojaelement_btn.textContent="Remover";
    console.log(newlojaelement_btn);

    var newlojaelement_div=document.createElement("div");
    newlojaelement_div.setAttribute("class","loja");
    console.log(newlojaelement_div);
    newlojaelement_div.appendChild(newlojaelement_label);
    newlojaelement_div.appendChild(newlojaelementurl_label);
    newlojaelement_div.appendChild(newlojaelement_input);
    newlojaelement_div.appendChild(newlojaurlelement_input);
    newlojaelement_div.appendChild(newlojaelement_btn);
    console.log(newlojaelement_div);
    var inserirlojaDiv=document.getElementById("lojas");
    console.log(inserirlojaDiv);
    inserirlojaDiv.appendChild(newlojaelement_div);
    }
    
}

$(document).ready(function(){
    // File type validation
        $("#fileInput").change(function(){
            var fileLength = this.files.length;
            var match= ["image/jpeg","image/png","image/jpg","image/gif"];
            var i;
            for(i = 0; i < fileLength; i++){ 
                var file = this.files[i];
                var imagefile = file.type;
                if(!((imagefile==match[0]) || (imagefile==match[1]) || (imagefile==match[2]) || (imagefile==match[3]))){
                    alert('Please select a valid image file (JPEG/JPG/PNG/GIF).');
                    $("#fileInput").val('');
                    return false;
                }
            }
        });
});