"use strict";




function BacklogEntry(props) {
  return (
    <div className="backlog_entry">
      {props.title} <br></br>
      <img  className="backlog_image" src={props.image} /> <br></br>
      Genre: {props.genre} <br></br>
      Ownership Status: {props.ownership_status}<br></br>
      Play Status: {props.play_status}<br></br>
      Playing On: {props.platform}<br></br>
    </div>
  );
}

function BacklogContainer() {
  const [backlogs, updateBacklogs] = React.useState([]);

  React.useEffect(() => {
    fetch("/api/backlog")
      .then((response) => response.json())
      .then((data) => updateBacklogs(data));
  }, []);

  const backlogEntries = [];
  console.log(backlogs)

  for (const backlog of backlogs) {
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

  return <div>{backlogEntries}</div>;
}

ReactDOM.render(<BacklogContainer />, document.getElementById("container"));
















