<script>
    import { createEventDispatcher, onMount } from 'svelte';
    import { incexpList} from "../../../store.js";

  
    export let value, required = true
    export let position_id;
    export let header_id;
    export let inPlaceType;
  
    const dispatch = createEventDispatcher()
    let editing = false, original
  
    onMount(() => {
      original = value
    })
  
    function edit() {
      editing = true
    }
  
    function submit() {
          if (value != original) {
              dispatch('submit', value)

              // console.log(header_id);
              // console.log(position_id);
              
              $incexpList
              .filter((header_row) => header_row['header_id'] ===  header_id)[0]['positions']
              .filter((position_row) => position_row['position_id'] === position_id)[0][inPlaceType] = value;
              
              // console.log($incexpList.filter((header_row) => header_row['header_id'] ===  header_id));

          }
          
      editing = false
    }
  
    function keydown(event) {
      if (event.key == 'Escape') {
        event.preventDefault()
        value = original
        editing = false
      }
    }
      
      function focus(element) {
          element.focus()
      }

  </script>
  
  {#if editing}
    <div class="col">
            <form 
            on:submit|preventDefault={submit} 
            on:keydown={keydown}
            >
            <input bind:value on:blur={submit} {required} use:focus/>
        </form>
    </div>
  {:else}
    <div class="col" on:click={edit} on:keydown={keydown}>{value}</div>
  {/if}
  
  <style>
    input {
      border: none;
      background: none;
      font-size: inherit;
      color: inherit;
      font-weight: inherit;
      text-align: inherit;
      box-shadow: none;
    }
  </style>
  