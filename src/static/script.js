let board = [
  [" ", " ", " "],
  [" ", " ", " "],
  [" ", " ", " "],
];
let gameActive = true;

function renderBoard() {
  $("#board").empty();
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      $("#board").append(
        `<div class="cell" data-row="${i}" data-col="${j}">${board[i][j]}</div>`
      );
    }
  }
}

function showPopup(message) {
  $("#popup-message").text(message);
  $("#popup").show();
}

function makeMove(row, col) {
  if (gameActive && board[row][col] === " ") {
    $("#status").text("AI is thinking...");
    $.ajax({
      url: "/make_move",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({ board: board, row: row, col: col }),
      success: function (response) {
        board = response.board;
        renderBoard();

        if (response.status === "human_win") {
          showPopup("Congratulations! You win!");
          gameActive = false;
        } else if (response.status === "ai_win") {
          showPopup("AI wins! Better luck next time.");
          gameActive = false;
        } else if (response.status === "tie") {
          showPopup("It's a tie!");
          gameActive = false;
        } else {
          $("#status").text("Your turn! Click a cell to make a move.");
        }
      },
    });
  }
}

function resetGame() {
  board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "],
  ];
  gameActive = true;
  renderBoard();
  $("#status").text("Your turn! Click a cell to make a move.");
}

$(document).ready(function () {
  renderBoard();

  $("#board").on("click", ".cell", function () {
    if (gameActive) {
      let row = $(this).data("row");
      let col = $(this).data("col");
      makeMove(row, col);
    }
  });

  $("#reset").on("click", resetGame);

  $("#close-popup").on("click", function () {
    $("#popup").hide();
    resetGame();
  });
});
