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
                    let name = html.find("#name")[0].value;
                    let damage = html.find("#damage")[0].value;
                    let dex = html.find("#dex")[0].checked;
                    let agile = html.find("#agile")[0].checked;
                    let dType = html.find("#dType")[0].checked;
                    let strikes = html.find("#strikes")[0].checked; // TODO: MULTIPLE STRIKES

                    // Roll Attack
                    let score = dex ? actor.data.data.abilities.dex.mod : actor.data.data.abilities.str.mod;
                    let prof = actor.data.items.find(item => item.name === "Improvised Weapons" && item.type === "martial").data.proficient.value;
                    let ab = dex ? "Dexterity" : "Strength";
                    let train;

                    // Assign proficiency name from level.
                    switch (prof) {
                        case 0:
                            train = "Untrained";
                            break;
                        case 1:
                            train = "Trained";
                            break;
                        case 2:
                            train = "Expert";
                            break;
                        case 3:
                            train = "Master";
                            break;
                        case 4:
                            train = "Legendary";
                            break;
                    }
                    prof = prof * 2 + actor.data.data.details.level.value;

                    let rollString = `1d20 + ${score + prof}`;
                    let roll = new Roll(rollString).roll();

                    roll.toMessage({
                        flags: {
                            core: {
                                "canPopout": true
                            },
                            pf2e: {
                                context: {
                                    actor: actor.id,
                                    type: "attack-roll",
                                    rollMode: "roll"
                            }
                        }
                        },
                        speaker: {
                            actor: actor.id,
                            alias: actor.name,
                            scene: game.user.viewedScene,
                            token: actor.data.token
                        },
                        flavor: `<b>Strike: ${name}</b><div class=\"tags\"><span class=\"tag tag_secondary\">${ab} +${score}</span><span class=\"tag tag_secondary\">${train} +${prof}</span></div>`,
                        content: `${roll.total}`
                    });
                }
            },
            saveWep: {
                label: "Save Weapon",
                callback: (html) => {
                    let name = html.find("#name")[0].value;
                    let damage = html.find("#damage")[0].value;
                    let dex = html.find("#dex")[0].checked;
                    let agile = html.find("#agile")[0].checked;
                    let dType = html.find("#dType")[0].checked;
                }
            }
        }
    }).render(true)
}