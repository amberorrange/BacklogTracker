"use strict";

const BacklogEntry = (props) => {
  return (
    <div className="backlog_entry">
      {props.title} <br></br>
      <img  className="backlog_image" src={props.image} /> <br></br>
      Genre: {props.genre} <br></br>
      Ownership Status: {props.ownership_status}<br></br>
      Play Status: {props.play_status ? 'Currently Playing' : 'Not Playing'}<br></br>
      Playing On: {props.platform}<br></br>
    </div>
  );
}

const FilterOption = ({ options, disabledLabel }) => {
  return (
    <React.Fragment>
       <option value="" defaultValue disabled>
        {disabledLabel}
      </option>
      <option value="All" key="All">All</option>
      {options.map((option) => (
        <option key={option} value={option}>{option}</option> 
      ))}
    </React.Fragment>
  )
}

const Select = (props) => {
  return (
    <div>
      <select value={props.value} onChange={props.onchange}>
        <FilterOption
          disabledLabel=""
          options={props.options}
        />
      </select>
    </div>
  )
}

// const Select = ({ value, onchange, options }) => {
//   return (
//     <div>
//       <select value={value} onChange={onchange}>
//         <FilterOption
//           options={options}
//         />
//       </select>
//     </div>
//   )
// }

const FilterOptions = (props) => {
  return (
    <div> 
      <Select 
        value={props.value}
        onchange={props.onchange}
        options={props.options}
      />
  </div>
  )
}

const BacklogContainer = () => {
  const [backlogs, updateBacklogs] = React.useState([]);
  const [displayedBacklogs, updateDisplayedBacklogs] = React.useState([]);
  const [genreFilter, updateGenreFilter] = React.useState(""); // ex.: 'fantasy', 'RPG'
  const [genresList, updateGenresList] = React.useState([])
  const [platformFilter, updatePlatformFilter] = React.useState("")
  const [platformsList, updatePlatformsList] = React.useState([])
  const [ownershipFilter, updateOwnershipFilter] = React.useState("")
  const [ownershipList, updateOwnershipList] = React.useState([])
  const [playstatusFilter, updatePlaystatusFilter] = React.useState("")
  const [playstatusList, updatePlaystatusList] = React.useState([])


  React.useEffect(() => {
    fetch("/api/backlog")
      .then((response) => response.json())
      .then((data) => {console.log(data); return data})
      .then((data) => {
        // Load initial backlog data into component
        updateBacklogs(data);
        updateDisplayedBacklogs(data);
      });
  }, []);


  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.platform)
    updatedList = new Set(updatedList)
    updatePlatformsList([...updatedList, ...platformsList])
  }, [backlogs])

  React.useEffect(() => {
    console.log(platformFilter, 'THIS IS THE CURRENTLY SELECTED Platform!')
    let updatedDisplay = backlogs.filter((backlog) => backlog.platform === platformFilter)
    updateDisplayedBacklogs(updatedDisplay)
  }, [platformFilter])

  React.useEffect(() => {
    console.log(platformFilter, 'THIS IS THE CURRENTLY SELECTED Platform!')
  if (platformFilter === "All") {
    updateDisplayedBacklogs(backlogs)
    }
  }, [platformFilter])




  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.play_status ? 'Currently Playing' : 'Not Playing')
    updatedList = new Set(updatedList)
    updatePlaystatusList([...updatedList, ...playstatusList])
  }, [backlogs])

  React.useEffect(() => {
    console.log(playstatusFilter, 'THIS IS THE CURRENTLY SELECTED play status!')
    let updatedDisplay = backlogs.filter((backlog) => backlog.play_status ? 'Currently Playing' : 'Not Playing' === playstatusFilter)
    updateDisplayedBacklogs(updatedDisplay)
  }, [playstatusFilter])

  React.useEffect(() => {
    console.log(playstatusFilter, 'THIS IS THE CURRENTLY SELECTED playstatus!')
  if (playstatusFilter === "All") {
    updateDisplayedBacklogs(backlogs)
    }
  }, [playstatusFilter])




  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.ownership_status)
    updatedList = new Set(updatedList)
    updateOwnershipList([...updatedList, ...ownershipList])
  }, [backlogs])

  React.useEffect(() => {
    console.log(ownershipFilter, 'THIS IS THE CURRENTLY SELECTED OS Status!')
    let updatedDisplay = backlogs.filter((backlog) => backlog.ownership_status === ownershipFilter)
    updateDisplayedBacklogs(updatedDisplay)
  }, [ownershipFilter])

  React.useEffect(() => {
    console.log(ownershipFilter, 'THIS IS THE CURRENTLY SELECTED OS Status!')
  if (ownershipFilter === "All") {
    updateDisplayedBacklogs(backlogs)
    }
  }, [ownershipFilter])



  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.genre)
    updatedList = new Set(updatedList)
    updateGenresList([...updatedList, ...genresList])
  }, [backlogs])

  React.useEffect(() => {
    console.log(genreFilter, 'THIS IS THE CURRENTLY SELECTED GENRE!')
    let updatedDisplay = backlogs.filter((backlog) => backlog.genre === genreFilter)
    updateDisplayedBacklogs(updatedDisplay)
  }, [genreFilter])

  React.useEffect(() => {
    console.log(genreFilter, 'THIS IS THE CURRENTLY SELECTED GENRE!')
    if (genreFilter === "All") {
      updateDisplayedBacklogs(backlogs)
    }
  }, [genreFilter])



  const handleSelect = (e) => {
    updateGenreFilter(e.target.value)
    console.log(genreFilter)
  }

  const handleplatformSelect = (e) => {
    updatePlatformFilter(e.target.value)
    console.log(platformFilter)
  }

  const handleOwnershipSelect = (e) => {
    updateOwnershipFilter(e.target.value)
    console.log(ownershipFilter)
  }

  const handlePlaystatusSelect = (e) => {
    updatePlaystatusFilter(e.target.value)
    console.log(playstatusFilter)
  }


  // console.log(backlogs, '## BACKLOGS ##')
  // console.log(displayedBacklogs, '## DISPLAYEDBACKLOGS ##')
  // console.log(genreFilter, '## GENREFILTER SELECTION##')
  // console.log(genresList, '## GENRESLIST ##')

  // console.log(platformFilter, '## PLATFORMFILTER SELECTION##')
  // console.log(platformsList, '## PLATFORMSLIST ##')

  // console.log(ownershipFilter, '## OWNERSHIPFILTER SELECTION##')
  // console.log(ownershipList, '## OWNERSHIPLIST ##')

  console.log(playstatusFilter, '## play status FILTER SELECTION##')
  console.log(playstatusList, '## play status LIST ##')
  console.log(displayedBacklogs, '## DISPLAYEDBACKLOGS ##')


  const backlogEntries = [];
  for (const backlog of displayedBacklogs) {
    backlogEntries.push(
      <BacklogEntry
        key={backlog.backlog_id}
        title={backlog.game.title}
        image= {backlog.game.image}
        genre= {backlog.genre}
        ownership_status= {backlog.ownership_status}
        play_status={backlog.play_status}
        platform={backlog.platform}
      />
    );
  }

  return (
    <div>
      {backlogEntries} <br></br>
      
      Genres:
      <FilterOptions 
        value={genreFilter}
        onchange={handleSelect}
        options={genresList}
      />
      
      <br></br>
      Platforms:
      <FilterOptions 
        value={platformFilter}
        onchange={handleplatformSelect}
        options={platformsList}
      />


      <br></br>
      Ownership Status:
      <FilterOptions 
        value={ownershipFilter}
        onchange={handleOwnershipSelect}
        options={ownershipList}
      />



      <br></br>
      Play Status:
      <FilterOptions 
        value={playstatusFilter}
        onchange={handlePlaystatusSelect}
        options={playstatusList}
      />
    </div>
  )
};


ReactDOM.render(<BacklogContainer />, document.getElementById("container"));