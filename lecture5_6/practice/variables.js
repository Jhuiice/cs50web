// let has block scope the variable only exist inside that block and below it
// Let cannot be redefined anywhere in the block it was created in only in the children
var alex = function() {
    let name = "Alex"
    {
        let name = "Me"
        // second name created in child block
        console.log(name)
        {
            // child block relates to its parent
            console.log(name)
        }
    }
    console.log(name)
    
}
// this line only works when the variables defined with let is used inside its block
// Let scope is inherited by its children but parents do not have access to it
// console.log(name)

alex()

// Var has no block scope
// Any variables defined with var can be used at any level of the inherited tree 
// The root connects to everything in the function block
// Vars can also be redefined within another block let cannot be
var matt = function(){
    {
        var name = "Matt";

    }
    console.log(name);

}
matt()


var constatine = function(){
    const name = "Constatine";
    { 
        // the variable is redifined in this block which means the block is new to its presence
        // if this const was not defined it would inherit its parents name
        // console.log(name);
        const name = "Inner Block of Constatine";
        console.log(name);
    }
    console.log(name);
}

constatine()
