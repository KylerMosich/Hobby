main()

async function main(){
    let actor = game.actors.get(game.user.character.id);

    let dialogTemplate = `
    <h1>Improvised Weapon:</h1>
    <div style="display:flex;">
        <label for="name" style="flex:1; padding-left:5px">Name</label>
        <input style="flex:2" id="name" type="text" value="Glass Bottle" />
        <label for="damage" style="flex:1; padding-left:5px">Damage</label>
        <input style="flex:2" id="damage" type="text" value="1d4" />
    </div>
    <div style="display:flex;">
        <span style="flex:0.8;">Dex <input id="dex" type="checkbox" /></span>
        <span style="flex:0.8;">Agile <input id="agile" type="checkbox" /></span>
        <span style="flex:1.2;">D. Type <select id="dType">
        <option value="b">B</option>
        <option value="p">P</option>
        <option value="s">S</option>
        </select></span>
        <span style="flex:1.2;">Strikes <select id="strikes">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        </select></span>
    </div>
  `
    new Dialog({
        title: "Improvised Weapon Improviser",
        content: dialogTemplate,
        buttons: {
            rollAtk: {
                label: "Roll Attack",
                callback: async (html) => {

                }
        }
    }).render(true)
}