<script>
    import FormPosition from "./FormPosition.svelte";
    import FormPositionTab from "./FormPositionTab.svelte";
    import {range} from './range.js';

    let currentPositionNumber = 1;
    
    function addPosition(){
      if (currentPositionNumber < 10){
          currentPositionNumber += 1;  
      }  
    };

    function RemovePosition(){
      if (currentPositionNumber>1){
          currentPositionNumber -= 1;  
      }  
    };

</script>

<div>
  <button class="btn btn-secondary" type="button" on:click={addPosition}>Dodaj pozycję</button>
  <button class="btn btn-secondary" type="button" on:click={RemovePosition}>Usuń pozycję</button>
</div>

<div>

  <ul class="nav nav-tabs" id="positionTab" role="tablist">
    {#each range(1, currentPositionNumber + 1, 1) as i}
      <FormPositionTab positionTabId= {i}/>  
    {/each}
  </ul>


  <div class="tab-content" id="positionContent">
    {#each range(1, currentPositionNumber + 1, 1) as i}
      <FormPosition position_id={i}/>
    {/each}
  </div>

</div>