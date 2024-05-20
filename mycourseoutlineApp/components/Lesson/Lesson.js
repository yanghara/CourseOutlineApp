import { Button, Card, Chip, Divider, List, Menu, Searchbar, PaperProvider } from "react-native-paper";
import MyStyle from "../../styles/MyStyle";
import APIs, { endpoints } from "../../configs/APIs";
import { useEffect, useState } from "react";
// import Item from "../utils/items";
import moment from 'moment';

import { View, Text, ActivityIndicator, ScrollView, TouchableOpacity, Image } from "react-native";

const Lesson = () => {
    const [outlines, setOutline] = useState([]);
    const [loading, setLoading] = useState(false);
    const [page, setPage] = useState(1);
    const [visible, setVisible] = useState(false);
    const openMenu = () => setVisible(true);
    const closeMenu = () => setVisible(false);

    const loadOutline = async () => {
        if (page > 0) {
            setLoading(true);
            try {
                let url = `${endpoints['outlines']}?page=${page}`;
                
                let res = await APIs.get(url);
                if (res.data.next === null)
                    setPage(0);
    
                if (page === 1)
                    setOutline(res.data.results);
                else
                    setOutline(current => {
                        return [...current, ...res.data.results];
                    });                
            } catch (ex) {
                console.error(ex);
            } finally {
                setLoading(false);
            }
        }
    }

    const isCloseToBottom = ({layoutMeasurement, contentOffset, contentSize}) => {
        const paddingToBottom = 20;
        return layoutMeasurement.height + contentOffset.y >=
          contentSize.height - paddingToBottom;
    };

    const loadMore = ({nativeEvent}) => {
        if (!loading && page > 0 && isCloseToBottom(nativeEvent)) {
                setPage(page + 1);
        }
    }

    useEffect(() => {
        loadOutline();
    }, [page]);

    const search = (value, callback) => {
        setPage(1);
        callback(value);
    }
    return (
        <View style={MyStyle.container}>
            <Text style={[MyStyle.subject,  MyStyle.margin]}>DANH MỤC ĐỀ CƯƠNG</Text>
            <View style={MyStyle.margin}>
                <Searchbar placeholder="Nhập từ khóa..." />
            </View>
            <ScrollView onScroll={loadMore}>
                {loading && <ActivityIndicator/>}
                {outlines.map(l => <TouchableOpacity key={l.id} >
                    <Card style={MyStyle.margin}>
                        <Card.Cover source={{ uri: l.image }} />
                        <Card.Title title={l.name} />
                        <Card.Content>
                        <Text variant="titleLarge">Credit: {l.credit}</Text>
                        <Text variant="bodyMedium">Overview: {l.overview}</Text>
                        </Card.Content>
                    </Card>
                </TouchableOpacity>)}
            </ScrollView>
            <PaperProvider>
            <View
                style={{
                paddingTop: 50,
                flexDirection: 'row',
                justifyContent: 'center',
                }}>
                <Menu
                visible={visible}
                onDismiss={closeMenu}
                anchor={<Button onPress={openMenu}>Show menu</Button>}>
                <Menu.Item onPress={() => {}} title="Item 1" />
                <Menu.Item onPress={() => {}} title="Item 2" />
                <Divider />
                <Menu.Item onPress={() => {}} title="Item 3" />
                </Menu>
            </View>
            </PaperProvider>
        </View>
    )
};
export default Lesson;