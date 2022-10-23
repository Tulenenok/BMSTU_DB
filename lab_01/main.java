import com.sun.xml.internal.bind.v2.runtime.unmarshaller.XsiNilLoader;

import java.io.FileWriter;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.List;


public class main {
//  стандартный главный класс в Java
    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost:5432/lab_1";
        String user = "postgres";
        String password = "112132";

//  массивы для генерации элементов таблицы материалов
        String[] details = {"Уголок 10*10*100", "Уголок 10*10*200", "Уголок 15*15*100", "Уголок 15*15*200", "Уголок 20*20*100",
                "Уголок 20*20*200", "Профиль 20*10*150", "Профиль 20*20*150", "Профиль 20*20*200", "Профиль 40*20*200",
                "Лист 100*100*5", "Лист 100*200*5", "Лист 200*200*5", "Лист 200*400*5", "Труба D10 L2000", "Труба D15 L2000",
                "Труба D20 L2000", "Труба D40 L4000", "Труба D45 L5000", "Труба D50 L5000"};
        String[] mats = {"Сталь Ст10", "Сталь Ст15", "Сталь Ст20", "Сталь Ст30", "Сталь Ст35", "Сталь Ст40", "Сталь Ст45",
                "Алюминий", "Железо оцинкованное", "Железо", "Бронза"};
//  массивы для генерации физических лиц
        String[] fam = {"Иванов", "Петров", "Сидоров", "Николаев", "Степанов", "Лопухин", "Васильев", "Томилов", "Локтев", "Ванин"};
        String[] imya = {"Иван", "Степан", "Василий", "Федор", "Никита", "Петр", "Олег", "Федот", "Кузьма", "Лев"};
        String[] otch = {"Иванович", "Степанович", "Васильевич", "Федорович", "Петрович", "Олегович", "Маратович", "Кузьмич", "Анатольевич", "Федотович"};
//  шаблоны запросов для наполнения таблиц БД
        String s1 = "insert into lab_1.building_materials (code, title, material, price, min_quant, is_deleted, inp_date)" +
                "values ('%s', '%s', '%s', %d, %d, 'N', current_date)";

        String s2 = "insert into lab_1.wh_stocks (whs_date, whs_no, mat_id, total, inp_date) values (current_date - %d, 4, %d, %d, current_date)";

        String s4 = "insert into lab_1.orders (order_date, order_no, person_id, order_state, shipment_date, price, inp_date) values (current_date - %d, %d, %d, %d, null, 0, current_date)";

        String s5 = "insert into lab_1.order_detail (order_id, mat_id, quant, price, inp_date) values (%d, %d, %d, %d, current_date)";

        String s6 = "insert into lab_1.order_shipments (order_id, person_id, mat_id, whs_no, shipment_date, quant, price, inp_date) values (%d, %d, %d, 4, current_date, %d, %d, current_date)";

        String s7 = "insert into lab_1.persons (name, sub_name, pat_name, inp_date) values ('%s', '%s', '%s', current_date)";

        Calendar calendar = new GregorianCalendar(2022, Calendar.AUGUST, 1);
//  соединение с БД в защищенном блоке с автоматическим закрытием соединений после завершения работы
//  con - объект соединения с БД
//  st  - объект для выполнения запросов добавления/изменения/удаления данных
//  lst - объект для получения данных из таблиц БД
        try (Connection con = DriverManager.getConnection(url, user, password);
             Statement st = con.createStatement();
             Statement lst = con.createStatement();
             FileWriter file = new FileWriter("lab1-data.sql", false);) {
            con.setAutoCommit(true);  // установка режима автоматического подтверждения транзакций

            file.write("delete from order_shipments;\n");
            file.write("delete from order_detail;\n");
            file.write("delete from orders;\n");
            file.write("delete from wh_stocks;\n");
            file.write("delete from building_materials;\n");
//  удаление "старых" данных
            st.execute("delete from lab_1.order_shipments");
            st.execute("delete from lab_1.order_detail");
            st.execute("delete from lab_1.orders");
            st.execute("delete from lab_1.wh_stocks");
            st.execute("delete from lab_1.building_materials");
            st.execute("delete from lab_1.persons");

            for (String f : fam) {
                for (String i : imya) {
                    for (String o : otch) {
                        String sql = String.format(s7, f, i, o);
                        st.execute(sql);
                    }
                }
            }
            List persons = new ArrayList();
            ResultSet data = lst.executeQuery("select * from lab_1.persons");
            while (data.next()) {
                Person person = new Person();
                person.idx = data.getInt("person_id");
                person.fam = data.getString("name");
                person.imya = data.getString("sub_name");
                person.otch = data.getString("pat_name");

                persons.add(person);
            }

//  заполнение таблицы материалов
            for (String det : details)
                for (String mat : mats) {
                    String sql = String.format(s1, rnd(1000000000), det, mat, rnd(100, 500), rnd(50));
                    file.write(sql + ";\n");
                    st.execute(sql);
                }
            file.write("\n");
//  заполнение таблицы складских запасов
            List mList = new ArrayList();
            data = lst.executeQuery("select * from lab_1.building_materials");
            while (data.next()) {
                Material material = new Material();
                material.idx = data.getInt("mat_id");
                material.price = data.getInt("price");
                mList.add(material);  // создание списка материалов в памяти для исключения повторных запросов к БД
//  заполнение таблицы складских остатков по дням от текущей даты минус 1 день до 30 дней назад
                for (int day = 1; day < 31; day++) {
                    String sql = String.format(s2, day, material.idx, rnd(1000));
                    file.write(sql + ";\n");
                    st.execute(sql);
                }
            }
            file.write("\n");
//  заполнение таблицы заказов
            for (int n = 1; n < 1501; n++) {
                int day = rnd(1, 30);
                Person person = (Person) persons.get(rnd(2, persons.size()));
                String sql = String.format(s4, day, rnd(100000), person.idx, 1);
                file.write(sql + ";\n");
                st.execute(sql);
            }
            file.write("\n");
//  заполнение таблиц состава заказов и отгрузки заказов
            data = lst.executeQuery("select * from lab_1.orders");
            String sql = "";
            while (data.next()) {
                int idx = data.getInt("order_id");
                int state = rnd(1, 5) < 4 ? 2 : 1;  // генерация признака отгрузки заказа: 1 - заказ принят, 2 - отгружен
                int order_price = 0;     // итоговая цена заказа = сумма(количество материалов * цена изделия)
                int shipment_price = 0;  // итоговая сумма отгрузки = сумма(количество отгруженных  * цена изделия)
//  состав заказа формируется случайным образом от 2 до 9 наименований в заказе
                for (int n = 1; n < rnd(2, 10); n++) {
                    Material material = (Material) mList.get(rnd(mList.size()));
                    int quant = rnd(10, 50);  // генерация количества выбранного материала в составе заказа
                    int price = quant * material.price;
                    order_price += price;

                    sql = String.format(s5, idx, material.idx, quant, price);
                    file.write(sql + ";\n");

                    st.execute(sql);  // добавление записи в состав заказа
//  если статус заказа (order_state) "отгружен", то генерируем запись об отгрузке материала
                    if (state == 2) {
                        int shipment = quant - rnd(5);
                        shipment = shipment < 0 ? 0 : shipment;  // количество отгруженного, считаем, что может быть "недогруз"
                        Person person = (Person) persons.get(rnd(2, persons.size()));

                        sql = String.format(s6, idx, person.idx, material.idx, shipment, shipment * material.price);
                        file.write(sql + ";\n");
                        st.execute(sql);  // добавление записи об отгрузке материала из состава заказа
                        shipment_price += shipment * material.price;
                    }
                }
//  формирование и выполнение запроса на изменение статуса и итоговых цен в заказе
                sql = String.format("update lab_1.orders set price = %d, shipment_price = %d, order_state = %d where order_id = %d",
                        order_price, shipment_price, state, idx);
                file.write(sql + ";\n");
                st.execute(sql);
            }
            file.flush();
        } catch (SQLException | IOException e) {
            System.out.println(e.getMessage());  // обработка возможных ошибок
        }
    }
//  функции генерации случайных чисел
    public static int rnd(int max)
    {
        return (int) (Math.random() * max);
    }

    public static int rnd(int min, int max)
    {
        max -= min;
        return (int) (Math.random() * max) + min;
    }
}
//  дополнительный класс для хранения в памяти данных о материале
class Material {
    int idx;
    int price;
}

class Person {
    int idx;
    String fam;
    String imya;
    String otch;
}