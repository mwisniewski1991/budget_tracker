<script>
    import FormPosition from "./FormPosition.svelte";
</script>

<ul class="nav nav-tabs" id="positionTab" role="tablist">
    <li class="nav-item" role="presentation">
      <button class="nav-link active" id="home-tab" data-bs-toggle="tab" data-bs-target="#pos_1" type="button" role="tab" aria-controls="pos_1" aria-selected="true">Poz 1</button>
    </li>

    <li class="nav-item" role="presentation">
      <button class="nav-link" id="contact-tab" data-bs-toggle="tab" data-bs-target="#pos_2" type="button" role="tab" aria-controls="pos_2" aria-selected="false">Poz 2</button>
    </li>
</ul>


<div class="tab-content" id="positionContent">
    
    <FormPosition position_id=1/>
    <FormPosition position_id=2/>



</div>