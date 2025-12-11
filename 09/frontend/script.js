// 設定: APIのURL
const API_URL = "http://127.0.0.1:8888/api/contacts";

// READ: データの取得と表示
// ページ読み込み完了時に一覧を取得
document.addEventListener("DOMContentLoaded", fetchContacts);

async function fetchContacts() {
  try {
    // Fetch APIでGETリクエスト
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("データの取得に失敗しました");

    const contacts = await response.json();
    renderList(contacts);
  } catch (error) {
    console.error("Error:", error);
    alert(
      "サーバーに接続できませんでした。Flaskアプリが起動しているか確認してください。",
    );
  }
}

// 取得したデータをHTMLリストとして描画する関数
function renderList(contacts) {
  const listElement = document.getElementById("contact-list");
  listElement.innerHTML = ""; // リストを一旦クリア

  contacts.forEach((contact) => {
    const li = document.createElement("li");

    // 表示内容の構築
    li.innerHTML = `
            <div class="contact-info">
                <strong>${escapeHtml(contact.name)}</strong><br>
                <small>📞 ${escapeHtml(contact.phone)} / ✉️ ${escapeHtml(
      contact.email,
    )}</small>
            </div>
            <div>
                <button class="btn-edit" onclick="startEdit(${
                  contact.id
                }, '${escapeHtml(contact.name)}', '${escapeHtml(
      contact.phone,
    )}', '${escapeHtml(contact.email)}')">編集</button>
                <button class="btn-delete" onclick="deleteContact(${
                  contact.id
                })">削除</button>
            </div>
        `;
    listElement.appendChild(li);
  });
}

// CREATE: 新規登録
async function createContact() {
  const name = document.getElementById("name").value;
  const phone = document.getElementById("phone").value;
  const email = document.getElementById("email").value;

  if (!name) {
    alert("氏名は必須です");
    return;
  }

  const newContact = { name, phone, email };

  try {
    // Fetch APIでPOSTリクエスト
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // JSON形式であることを指定
      },
      body: JSON.stringify(newContact), // オブジェクトをJSON文字列に変換
    });

    if (!response.ok) throw new Error("登録に失敗しました");

    // 成功したらフォームをクリアして一覧を再取得
    resetForm();
    fetchContacts();
  } catch (error) {
    console.error("Error:", error);
    alert("登録中にエラーが発生しました");
  }
}

// DELETE: 削除
async function deleteContact(id) {
  if (!confirm("本当に削除しますか？")) return;

  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) throw new Error("削除に失敗しました");

    fetchContacts(); // 一覧更新
  } catch (error) {
    console.error("Error:", error);
    alert("削除中にエラーが発生しました");
  }
}

// UPDATE: 更新 (編集モードへの切り替えと送信)
// 編集ボタンを押した時の処理（フォームに値を埋めてボタンを切り替え）
function startEdit(id, name, phone, email) {
  document.getElementById("form-title").innerText = "編集モード";
  document.getElementById("contact-id").value = id;
  document.getElementById("name").value = name;
  document.getElementById("phone").value = phone;
  document.getElementById("email").value = email;

  // ボタンの表示切り替え
  document.getElementById("btn-add").style.display = "none";
  document.getElementById("btn-update").style.display = "inline-block";
  document.getElementById("btn-cancel").style.display = "inline-block";
}

// 更新ボタンを押した時の処理
async function updateContact() {
  const id = document.getElementById("contact-id").value;
  const name = document.getElementById("name").value;
  const phone = document.getElementById("phone").value;
  const email = document.getElementById("email").value;

  const updateData = { name, phone, email };

  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updateData),
    });

    if (!response.ok) throw new Error("更新に失敗しました");

    resetForm();
    fetchContacts();
  } catch (error) {
    console.error("Error:", error);
    alert("更新中にエラーが発生しました");
  }
}

// ユーティリティ
// フォームを初期状態に戻す
function resetForm() {
  document.getElementById("form-title").innerText = "新規登録";
  document.getElementById("contact-id").value = "";
  document.getElementById("name").value = "";
  document.getElementById("phone").value = "";
  document.getElementById("email").value = "";

  document.getElementById("btn-add").style.display = "inline-block";
  document.getElementById("btn-update").style.display = "none";
  document.getElementById("btn-cancel").style.display = "none";
}

// XSS対策: HTMLエスケープ処理
function escapeHtml(unsafe) {
  if (unsafe == null) return "";
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
