import json
import string
import sys
from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
from typing import ClassVar, NamedTuple, Protocol


class ReportData(Protocol):
    def resolve(self, template: str) -> str: ...
    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> "ReportData": ...


Value = str | int
FlatJSON = dict[str, Value]
JSONEntry = tuple[str, Value]


class Member(NamedTuple):
    ID: str
    NAME: str

    @classmethod
    def from_dict(cls, data: FlatJSON) -> list["Member"]:
        def is_member_field(item: JSONEntry) -> bool:
            (key, _) = item
            return key.startswith(("MEMBER_ID_", "MEMBER_NAME_"))

        member_dict = dict(filter(is_member_field, data.items()))
        member_len = len(member_dict) // 2

        members: list[Member] = []
        for i in range(1, member_len + 1):
            member_id = str(member_dict[f"MEMBER_ID_{i}"])
            member_name = str(member_dict[f"MEMBER_NAME_{i}"])
            members.append(Member(ID=member_id, NAME=member_name))

        return members


@dataclass
class ReportInfo(ReportData):
    CLASS_NO: int
    MY_ID: str
    MY_NAME: str
    GROUP_ID: str
    LEADER_ID: str
    LEADER_NAME: str
    MEMBERS: list[Member] = field(default_factory=list)

    def to_dict(self) -> FlatJSON:
        def exclude_member(item: JSONEntry) -> bool:
            (key, _) = item
            return key != "MEMBERS"

        d = dict(filter(exclude_member, vars(self).items()))
        if self.MEMBERS:
            for i, member in enumerate(self.MEMBERS, start=1):
                d[f"MEMBER_ID_{i}"] = member.ID
                d[f"MEMBER_NAME_{i}"] = member.NAME
        return d

    @classmethod
    def from_dict(cls, data: FlatJSON) -> "ReportInfo":
        members = Member.from_dict(data)

        return cls(
            CLASS_NO=int(data["CLASS_NO"]),
            MY_ID=str(data["MY_ID"]),
            MY_NAME=str(data["MY_NAME"]),
            GROUP_ID=str(data["GROUP_ID"]),
            LEADER_ID=str(data["LEADER_ID"]),
            LEADER_NAME=str(data["LEADER_NAME"]),
            MEMBERS=members,
        )

    def resolve(self, template: str) -> str:
        tpl = string.Template(template)
        return tpl.safe_substitute(**self.to_dict())

    def get_my_info_template(self) -> str:
        ret = f"""\
- 学籍番号：{self.MY_ID}
- 氏名：{self.MY_NAME}
- グループ：{self.GROUP_ID}
    - メンバー
        - {self.LEADER_ID} {self.LEADER_NAME}（チームリーダー）
"""
        for i in self.MEMBERS:
            ret += f"""
        - {i.ID} {i.NAME}
"""
        return ret


@dataclass
class ReportBody(ReportData):
    MY_INFO: str | None = None
    APP_SPEC_DESCRIBE: str = """\
- flaskを使ったフォトアルバム
- 画像をアップロードできる
- アップロードした画像にタグをつけられる
- アップロードした画像にコメントを書ける
- 画像検索ページでタグやコメントから画像を検索できる
- CSSで画面を見やすくする
"""
    APP_IMAGE: str = """\
- ここにトップページの手書きいらすと（top_page.jpegもMoodleへアップロードした）
- ここに画像リストページの手書きイラスト(image_list_page.jpeg)
- ここに画像アップロードページの手書きいらすと(upload_page.jpeg)
- ここに画像検索ページの手書きイラスト(search_page.jpeg)
"""
    WORK_FLOW: str = """\
- 画像をアップロードできる（担当：$MEMBER_ID_3 $MEMBER_NAME_3）
- アップロードした画像にタグをつけられる（主担当：$MEMBER_ID_1 $MEMBER_NAME_1，副担当：$MEMBER_ID_2 $MEMBER_NAME_2）
- アップロードした画像にコメントを書ける（主担当：$MEMBER_ID_2 $MEMBER_NAME_2，副担当：$MEMBER_ID_1 $MEMBER_NAME_1）
- 画像検索ページでタグやコメントから画像を検索できる（担当：$MEMBER_ID_4 $MEMBER_NAME_4）
- CSSで画面を見やすくする（担当：$MEMBER_ID_5 $MEMBER_NAME_5）
"""
    MY_WEEKLY_REPORT: str = """\
- (これはサンプルです)
- 画像を保管する仕様を愛知花子と話あって決めた
- 保管した画像がWebページに表示されるところまで愛知花子と共同作業して作った
    - プルリクエストへのリンク
    - 上のプルリクエストがマージされた
"""
    THANKS2MEMBER: str = """\
- 画像処理のベースプログラム実装を一緒にした($MEMBER_ID_2 $MEMBER_NAME_2)
- プルリクエストを処理してくれた（$MEMBER_ID_1 $MEMBER_NAME_1）
- 調べ物を手伝ってくれた($MEMBER_ID_5 $MEMBER_NAME_5)
"""
    MY_THOUGHTS_AND_NEXT_WORKS: str = """\
- 計画通りに作業は進んでいる
- 画像を取り扱う共通仕様は愛知花子と共同で作成したが，来週からは作業を分担してすすめる
"""

    def resolve(self, template: str) -> str:
        tpl = string.Template(template)
        return tpl.safe_substitute(**self.to_dict())

    def to_dict(self) -> dict:
        return vars(self)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "ReportBody":
        return cls(**data)


@dataclass
class Report:
    info: ReportInfo
    body: ReportBody

    TEMPLATE: ClassVar = """\
# オブジェクト指向プログラミングおよび演習 第$CLASS_NO回進捗レポート

## 作成者情報
$MY_INFO

## 仕様
$APP_SPEC_DESCRIBE

## アプリ完成イメージ
$APP_IMAGE

## 作業分担
$WORK_FLOW

## 作業報告
$MY_WEEKLY_REPORT

## グループ内でお世話になった人2〜3名を理由とともに挙げる
$THANKS2MEMBER

## 振り返り（感想含む）と次回までの作業予定
$MY_THOUGHTS_AND_NEXT_WORKS
"""

    def __post_init__(self) -> None:
        self.body.MY_INFO = self.info.get_my_info_template()

    def get_data(self) -> list[ReportData]:
        return [self.body, self.info]

    def resolve(self, target_data: list[ReportData] | None = None) -> str:
        data = target_data if target_data is not None else self.get_data()
        return reduce(lambda acc, d: d.resolve(acc), data, self.TEMPLATE)

    @classmethod
    def load(cls, file: Path) -> "Report":
        with file.open() as f:
            status: dict = json.load(f)

        info = ReportInfo.from_dict(status.get("basic_info", {}))
        body = ReportBody.from_dict(status.get("history", {}))
        return cls(info=info, body=body)

    def to_dict(self, *, flatten: bool = False) -> dict:
        if flatten:
            return {**self.info.to_dict(), **self.body.to_dict()}

        return {
            "basic_info": self.info.to_dict(),
            "history": self.body.to_dict(),
        }

    def save_as_json(self, file: Path) -> None:
        with file.open("w") as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)

    def save_as_text(self, file: Path, *, include_history: bool = True) -> None:
        data: list[ReportData] = self.get_data()

        if not include_history:
            data.remove(self.body)

        resolved_text = self.resolve(data)
        with file.open("w") as f:
            f.write(resolved_text)


class report_model:
    """テキストデータの管理(get,set)および保管(save,load)を行うクラス"""

    KEY_LIST: ClassVar[list[str]] = [
        "CLASS_NO",
        "MY_INFO",
        "APP_SPEC_DESCRIBE",
        "APP_IMAGE",
        "WORK_FLOW",
        "MY_WEEKLY_REPORT",
        "THANKS2MEMBER",
        "MY_THOUGHTS_AND_NEXT_WORKS",
    ]

    report: Report

    def __init__(self):
        status_file = Path("status.json")

        if not status_file.is_file():
            print("status.jsonファイルを準備してください")
            sys.exit(1)

        self.report = Report.load(status_file)
        print(self.report.to_dict(flatten=True).keys())

    def get_body(self) -> str:
        return self.report.resolve()

    def get_template_class_no(self) -> int:
        return self.report.info.CLASS_NO

    def get_template_my_info(self) -> str:
        return self.report.info.get_my_info_template()

    @staticmethod
    def get_template_app_spec_describe() -> str:
        return ReportBody.__dataclass_fields__["APP_SPEC_DESCRIBE"].default

    @staticmethod
    def get_template_app_image() -> str:
        return ReportBody.__dataclass_fields__["APP_IMAGE"].default

    @staticmethod
    def get_template_work_flow() -> str:
        return ReportBody.__dataclass_fields__["WORK_FLOW"].default

    @staticmethod
    def get_template_my_weekly_report() -> str:
        return ReportBody.__dataclass_fields__["MY_WEEKLY_REPORT"].default

    @staticmethod
    def get_template_thanks2member() -> str:
        return ReportBody.__dataclass_fields__["THANKS2MEMBER"].default

    @staticmethod
    def get_template_my_thoughts_and_next_works() -> str:
        return ReportBody.__dataclass_fields__["MY_THOUGHTS_AND_NEXT_WORKS"].default

    def get_text_by_key(self, key_name: str) -> str:
        value = self.report.to_dict(flatten=True)
        return str(value[key_name])

    def set_text_by_key(self, key_name: str, value: str) -> None:
        if key_name == "CLASS_NO":
            self.report.info.CLASS_NO = int(value)
        else:
            self.report.body.__setattr__(key_name, value)

    def save_file(self, file_text: str, file_name: str | None = None) -> None:
        """マークダウンファイルとhistoryを保存"""
        if file_name is None:
            file_name = f"{self.report.info.MY_ID}{self.report.info.MY_NAME}.md"

        with Path(file_name).open("w") as f:
            f.write(file_text)

        status_file = Path("status.json")
        self.report.save_as_json(status_file)

    def save_file_without_history(self, file_text: str, file_name: str | None = None) -> None:
        """マークダウンファイルのみ保存"""
        if file_name is None:
            file_name = f"{self.report.info.MY_ID}{self.report.info.MY_NAME}.md"

        with Path(file_name).open("w") as f:
            f.write(file_text)
