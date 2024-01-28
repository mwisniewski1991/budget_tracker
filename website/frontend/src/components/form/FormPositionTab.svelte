<script>
    export let positionTabId;
    export let selected = "false";


    function selectClass(position){
        if(position == 1){
            return "nav-link active"
        }else{
            return "nav-link"
        }
    }

 
    let html_position_id = `pos_${positionTabId}`
    let html_position_id_hash = `#pos_${positionTabId}`
    
</script>



<li class="nav-item" role="presentation">
    <button class={selectClass(positionTabId)} id="home-tab" data-bs-toggle="tab" data-bs-target={html_position_id_hash} type="button" role="tab" aria-controls={html_position_id} aria-selected={selected}>
        Poz {positionTabId}
    </button>
</li>