(function(){var r=document.documentElement,k="demo-theme";try{var s=localStorage.getItem(k);if(s)r.dataset.theme=s}catch(e){}
function menu(open){var b=document.querySelector("[data-menu]"),m=document.getElementById("menu");if(!b||!m)return;
 b.setAttribute("aria-expanded",open);b.setAttribute("aria-label",open?"Cerrar menú":"Abrir menú");m.hidden=!open;if(open){var a=m.querySelector("a");a&&a.focus()}}
document.addEventListener("keydown",function(e){if(e.key==="Escape"){var b=document.querySelector("[data-menu]");if(b&&b.getAttribute("aria-expanded")==="true"){menu(false);b.focus()}}});
document.addEventListener("click",function(e){
 var mb=e.target.closest("[data-menu]");if(mb){menu(mb.getAttribute("aria-expanded")!=="true");return}
 if(!e.target.closest("#menu"))menu(false);
 if(e.target.closest("[data-toggle]")){var d=r.dataset.theme?r.dataset.theme==="dark":matchMedia("(prefers-color-scheme: dark)").matches;
  r.dataset.theme=d?"light":"dark";try{localStorage.setItem(k,r.dataset.theme)}catch(e){}}
 var b=e.target.closest("[data-filter]");if(b){var f=b.dataset.filter;
  document.querySelectorAll("[data-filter]").forEach(function(x){x.setAttribute("aria-pressed",x===b)});
  document.querySelectorAll("[data-cat]").forEach(function(li){li.hidden=f!=="todo"&&li.dataset.cat!==f});}
});})();
