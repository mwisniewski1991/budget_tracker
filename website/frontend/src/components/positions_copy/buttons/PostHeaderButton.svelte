<script>
    export let headerIDtoEdit;
    import { incexpList } from "../../store.js";


    async function editHeader(headerID, val){
        
        console.log($incexpList.filter((header_row) => header_row['header_id'] ===  headerID));

        // const parameters = new URLSearchParams({headerid: headerID});
        // const resposne = await fetch(`/api/v1/position-delete?${parameters}`, {method:"DELETE"})
        // const results =  await resposne.json();
        // location.reload()
    };


</script>

<button type="button" class="btn btn-info" on:click={editHeader(headerIDtoEdit, false)}>CHANGE</button>            


